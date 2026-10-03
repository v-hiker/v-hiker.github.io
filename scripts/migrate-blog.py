#!/usr/bin/env python3
"""Preserve the original static Hexo site at /blog/ without touching its old URLs.

The source commit is pinned because the root index.html is now a character page.
Existing comments configuration is copied as-is and never printed by this tool.
Run from any directory with: python scripts/migrate-blog.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET


SOURCE_COMMIT = "ff4c4fa7052d01c3c3de0deaf4d09db72ff3f75a"
SITE_ROOT = Path(__file__).resolve().parents[1]
BLOG_ROOT = SITE_ROOT / "blog"
BASE = "/blog/"
LOCAL_HOSTS = {"tamako.top", "www.tamako.top", "v-hiker.github.io"}
TEXT_EXTENSIONS = {".html", ".css", ".js", ".xml", ".json", ".webmanifest", ".svg"}
SKIP_TOP_LEVEL = {".git", "blog", "assets", "scripts"}
ATTRIBUTE_URL = re.compile(
    r"(?P<prefix>\b(?:href|src|poster|action|data-src)\s*=\s*)(?P<quote>[\"'])(?P<url>[^\"']*)(?P=quote)",
    re.IGNORECASE,
)
CSS_URL = re.compile(r"url\(\s*(?P<quote>[\"']?)(?P<url>[^\s\"')]+)(?P=quote)\s*\)", re.IGNORECASE)
THEME_CDN = re.compile(r"^(?:https?:)?//cdn\.jsdelivr\.net/npm/hexo-theme-keep@3\.6\.1/source/(.+)$")


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=SITE_ROOT)


def source_paths(ref: str) -> list[str]:
    paths = git("ls-tree", "-r", "--name-only", "-z", ref).decode("utf-8").split("\0")
    return [
        path for path in paths
        if path
        and PurePosixPath(path).parts[0] not in SKIP_TOP_LEVEL
        and PurePosixPath(path).name.lower() not in {"cname", "debug.log"}
        and not PurePosixPath(path).name.lower().startswith("readme")
    ]


def rebase_url(url: str) -> str:
    """Rebase actual site references; leave anchors and unrelated origins alone."""
    theme_match = THEME_CDN.match(url)
    if theme_match:
        relative = theme_match.group(1)
        if (SITE_ROOT / relative).is_file():
            return BASE + relative
    if url.startswith(BASE):
        return url
    if url.startswith("/") and not url.startswith("//"):
        return BASE + url.lstrip("/")
    parsed = urlsplit(url)
    if parsed.hostname in LOCAL_HOSTS:
        path = parsed.path
        if not path.startswith(BASE):
            path = BASE + path.lstrip("/")
        result = path
        if parsed.query:
            result += "?" + parsed.query
        if parsed.fragment:
            result += "#" + parsed.fragment
        return result
    return url


def rewrite_text(text: str, relative: str) -> str:
    if relative == "js/libs/pjax.min.js":
        # The committed local bundle has three mis-cased method calls. The old
        # site used the CDN bundle, so this only surfaced when moving offline.
        text = text.replace("this.loadurl", "this.loadUrl")
    text = ATTRIBUTE_URL.sub(
        lambda match: match["prefix"] + match["quote"] + rebase_url(match["url"]) + match["quote"],
        text,
    )
    text = CSS_URL.sub(
        lambda match: "url(" + match["quote"] + rebase_url(match["url"]) + match["quote"] + ")",
        text,
    )
    # KEEP concatenates root + search.xml when fetching the local search index.
    if relative.endswith(".html"):
        text = re.sub(r'("root"\s*:\s*")/("\s*[,}])', r'\1/blog/\2', text)
    if relative == "search.xml":
        text = re.sub(
            r"(<url>)([^<]*)(</url>)",
            lambda match: match[1] + rebase_url(match[2]) + match[3],
            text,
        )
    if relative == "imgs/site.webmanifest":
        manifest = json.loads(text)
        for icon in manifest.get("icons", []):
            # The old manifest incorrectly referenced icons at the domain root.
            name = PurePosixPath(urlsplit(icon.get("src", "")).path).name
            if (BLOG_ROOT / "imgs" / name).is_file():
                icon["src"] = BASE + "imgs/" + name
        manifest["scope"] = BASE
        manifest["start_url"] = BASE
        text = json.dumps(manifest, ensure_ascii=False, separators=(",", ":"))
    return text


class PageLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for attribute, value in attrs:
            if value and attribute in {"href", "src", "poster", "action", "data-src"}:
                self.urls.append((attribute, value))


def local_target(url: str, page_url: str) -> tuple[str, Path] | None:
    if url.startswith(("#", "javascript:", "mailto:", "tel:", "data:", "blob:")):
        return None
    resolved = urlsplit(urljoin("https://tamako.top" + page_url, url))
    if resolved.hostname not in LOCAL_HOSTS:
        return None
    path = unquote(resolved.path)
    target = SITE_ROOT / path.lstrip("/")
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    if not target.is_file() and not PurePosixPath(path).suffix:
        target = target / "index.html"
    return path, target


def audit(paths: list[str], ref: str) -> dict:
    missing: set[tuple[str, str]] = set()
    escaped: set[tuple[str, str]] = set()
    checked = 0
    utf8_without_bom = True
    source_hashes_intact = True
    html_pages = 0
    for relative in paths:
        original = git("show", f"{ref}:{relative}")
        current_original = SITE_ROOT / relative
        if relative != "index.html" and current_original.is_file():
            current_bytes = current_original.read_bytes()
            if current_original.suffix in TEXT_EXTENSIONS:
                # Windows Git can expand LF to CRLF when checking out text files.
                original = original.replace(b"\r\n", b"\n")
                current_bytes = current_bytes.replace(b"\r\n", b"\n")
            source_hashes_intact &= hashlib.sha256(original).digest() == hashlib.sha256(current_bytes).digest()
        copied = BLOG_ROOT / relative
        if copied.suffix not in TEXT_EXTENSIONS:
            continue
        raw = copied.read_bytes()
        utf8_without_bom &= not raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8")
        page_url = BASE + relative
        if copied.suffix == ".html":
            html_pages += 1
            page = PageLinks()
            page.feed(text)
            urls = [url for _, url in page.urls]
            if '"root":"/blog/"' not in text:
                escaped.add((relative, "KEEP.root"))
        elif copied.suffix == ".css":
            urls = [match["url"] for match in CSS_URL.finditer(text)]
        elif relative == "search.xml":
            urls = [item.text or "" for item in ET.fromstring(text).findall("entry/url")]
        elif copied.suffix == ".webmanifest":
            urls = [item["src"] for item in json.loads(text).get("icons", [])]
        else:
            urls = []
        for url in urls:
            result = local_target(url, page_url)
            if not result:
                continue
            path, target = result
            checked += 1
            if not path.startswith(BASE):
                escaped.add((relative, path))
            if not target.is_file():
                missing.add((relative, path))
    entries = ET.parse(BLOG_ROOT / "search.xml").getroot().findall("entry")
    return {
        "source_commit": ref,
        "base_path": BASE,
        "copied_files": len(paths),
        "html_pages": html_pages,
        "article_pages": len([path for path in paths if path.startswith("posts/") and path.endswith("/index.html")]),
        "search_entries": len(entries),
        "local_references_checked": checked,
        "references_outside_blog": [{"file": file, "url": url} for file, url in sorted(escaped)],
        "missing_local_references": [{"file": file, "url": url} for file, url in sorted(missing)],
        "text_utf8_without_bom": utf8_without_bom,
        "legacy_files_unchanged": source_hashes_intact,
        "legacy_text_comparison": "Git checkout line endings normalized to LF",
        "legacy_article_urls_preserved": all((SITE_ROOT / path).is_file() for path in paths if path.startswith("posts/")),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-ref", default=SOURCE_COMMIT)
    parser.add_argument("--check-only", action="store_true")
    options = parser.parse_args()
    paths = source_paths(options.source_ref)
    if not options.check_only:
        # Copy first, so manifest and CDN substitutions can see all local assets.
        for relative in paths:
            destination = BLOG_ROOT / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(git("show", f"{options.source_ref}:{relative}"))
        for relative in paths:
            destination = BLOG_ROOT / relative
            if destination.suffix in TEXT_EXTENSIONS:
                text = destination.read_bytes().decode("utf-8-sig")
                destination.write_bytes(rewrite_text(text, relative).encode("utf-8"))
    report = audit(paths, options.source_ref)
    (Path(__file__).parent / "blog-migration-report.json").write_bytes(
        (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )
    # Report contains only paths, counts and booleans; never configuration values.
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["references_outside_blog"] or report["missing_local_references"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
