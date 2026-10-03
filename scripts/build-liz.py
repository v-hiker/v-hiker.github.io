"""Generate the standalone /liz/ feature; deployment uses the committed HTML."""
import json
from html import escape
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'liz'
data = json.loads((ASSETS / 'content.json').read_text(encoding='utf-8'))


def e(value):
    return escape(str(value), quote=True)


def image(record, eager=False):
    with Image.open(ASSETS / record['file']) as picture:
        width, height = picture.size
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="../assets/liz/{e(record["file"])}" alt="{e(record["alt"])}" width="{width}" height="{height}" {loading}>'


def heading(overline, title, description=''):
    return f'<div class="section-heading"><p class="overline">{overline}</p><h2>{title}</h2>' + (f'<p>{description}</p>' if description else '') + '</div>'


def external(url, label, cls=''):
    return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span></a>'


people = ''.join(f'''<article class="person {e(person['key'])}"><figure class="person-picture">{image(person)}</figure><div class="person-text"><p class="person-instrument">{e(person['instrument'])} <span>{e(person['enInstrument'])}</span></p><h3>{e(person['name'])}<small lang="ja">{e(person['jaName'])}</small></h3><p>{e(person['description'])}</p><p class="person-voice">声优 / {e(person['cv'])}</p></div></article>''' for person in data['characters'])
worlds = ''.join(f'''<article class="world-row {e(world['key'])}"><figure class="world-picture">{image(world)}</figure><div class="world-copy"><p class="overline">{e(world['overline'])}</p><h3>{e(world['title'])}</h3><p>{e(world['description'])}</p></div></article>''' for world in data['worlds'])
listening = ''.join(f'''<article class="listen-point"><span class="listen-number" aria-hidden="true">0{i}</span><h3>{e(note['title'])}</h3><p>{e(note['description'])}</p></article>''' for i, note in enumerate(data['listening'], 1))
tracks = ''.join(f'''<a class="music-track" href="{e(track['url'])}" target="_blank" rel="noopener noreferrer"><span class="track-type">{e(track['type'])}</span><div><strong lang="ja">{e(track['title'])}</strong><small>{e(track['artist'])}</small></div><span class="track-arrow" aria-hidden="true">↗</span></a>''' for track in data['music'])
credits = ''.join(f'<div><dt>{e(record["label"])}</dt><dd>{e(record["value"])}</dd></div>' for record in data['credits'])
gallery = ''.join(f'''<button class="gallery-item" type="button" data-category="{e(record['category'])}" data-title="{e(record['title'])}" data-caption="{e(record['caption'])}" data-credit="{e(record['credit'])}" data-source="{e(record['source'])}" aria-label="放大：{e(record['title'])}">{image(record)}<span class="gallery-label"><span>{e(record['label'])}</span><strong>{e(record['title'])}</strong></span></button>''' for record in data['gallery'])
sources = ''.join(f'<li>{external(source["url"], e(source["title"]))}</li>' for source in data['sources'])
cover = data['images']['cover']
intro = data['images']['intro']
scene = data['images']['listening']
film = data['film']

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f7fbfc">
  <meta name="description" content="利兹与青鸟，关于霙与希美、双簧管与长笛。走进校园与童话交织的故事，收藏京都动画电影中的声音与画面。">
  <title>利兹与青鸟｜聆听两个人的距离。</title>
  <link rel="icon" href="../assets/liz/bird.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../assets/liz/style.css">
  <link rel="preload" as="image" href="../assets/liz/{e(cover['file'])}" fetchpriority="high">
  <script src="../assets/liz/app.js" defer></script>
</head>
<body class="liz-page">
  <a class="skip-link" href="#main">跳到正文</a>
  <header class="liz-header"><a class="liz-brand" href="#home" aria-label="利兹与青鸟，回到首页"><span>利兹与青鸟</span><small>LIZ AND THE BLUE BIRD</small></a><button class="liz-menu" type="button" aria-label="打开导航" aria-expanded="false" aria-controls="liz-nav"><span></span><span></span></button><nav class="liz-nav" id="liz-nav" aria-label="主导航"><a href="#about">故事</a><a href="#duet">霙与希美</a><a href="#worlds">两种世界</a><a href="#music">音乐</a><a href="#gallery">画廊</a></nav></header>
  <main id="main">
    <section class="cover" id="home" aria-labelledby="cover-title"><figure class="cover-art">{image(cover, eager=True)}</figure><div class="cover-copy"><p class="cover-eyebrow">LIZ AND THE BLUE BIRD</p><h1 id="cover-title">利兹与青鸟<small lang="ja">リズと青い鳥</small></h1><p class="cover-line">聆听，两个人的距离。</p><p class="cover-description">双簧管与长笛。<br>同一段旋律里，轻轻交错的两颗心。</p><div class="cover-actions"><a href="#about">走进故事 <span aria-hidden="true">↓</span></a><a href="#gallery">收藏画面 <span aria-hidden="true">↗</span></a></div></div><p class="cover-caption">A FILM BY NAOKO YAMADA <span>KYOTO ANIMATION · 2018</span></p></section>
    <div class="film-facts page-width"><div><span>日本上映</span><strong>{e(film['releaseDate'])}</strong></div><div><span>片长</span><strong>{e(film['runtime'])}</strong></div><div><span>监督</span><strong>山田尚子</strong></div><div><span>动画制作</span><strong>京都动画</strong></div></div>

    <section class="page-width section-space intro" id="about"><div class="intro-heading"><p class="overline">A STORY IN SOFT NOTES</p><h2>有些心情，<br>比语言更早响起。</h2></div><div class="intro-layout"><div class="intro-text">{''.join('<p>' + e(paragraph) + '</p>' for paragraph in data['introduction'])}<p class="intro-note">{e(data['introNote'])}</p></div><figure class="intro-image">{image(intro)}<figcaption>{e(intro['caption'])}</figcaption></figure></div></section>

    <section class="duet section-space" id="duet"><div class="page-width">{heading('OBOE / FLUTE', '霙与希美。', '她们总是一起，却有着各自感受世界的方式。')}<div class="duet-grid">{people}</div><p class="duet-note">双簧管与长笛，在合奏里相遇。<br>彼此的音色，也映出那些难以说清的心情。</p></div></section>

    <section class="worlds section-space page-width" id="worlds">{heading('TWO WORLDS, ONE MELODY', '校园与童话，轻轻叠在一起。')} {worlds}<p class="worlds-note">一部作品里的两种画风，两段故事里的同一份牵挂。</p></section>

    <section class="listening section-space" id="listening"><div class="page-width">{heading('VIEWING NOTES / 观影解读', '把声音调近一点。', '这些声画细节，是走近故事的几条线索。')}<div class="listening-grid">{listening}</div><figure class="listen-scene">{image(scene)}<figcaption>{e(scene['caption'])}</figcaption></figure></div></section>

    <section class="music section-space page-width" id="music">{heading('MUSIC & FILM', '当两种声音，成为同一段音乐。', '电影配乐、童话与吹奏乐曲，各自留下不同的色彩。')}<div class="music-list">{tracks}</div><p class="music-note">曲目链接通往官方音乐与唱片介绍。</p><div class="film-credits"><p class="overline">THE PEOPLE BEHIND THE FILM</p><dl>{credits}</dl></div><div class="film-links">{external('https://liz-bluebird.com/', '作品官网')}{external(data['trailerUrl'], '官方预告')}</div></section>

    <section class="gallery section-space" id="gallery"><div class="page-width"><div class="gallery-heading">{heading('COLLECTED FRAMES', '风经过，留下这些画面。', '来自原作的校园、童话与绘图。')}<div class="gallery-filters" role="group" aria-label="画廊分类"><button type="button" class="is-active" data-filter="all" aria-pressed="true">全部</button><button type="button" data-filter="school" aria-pressed="false">校园</button><button type="button" data-filter="fairytale" aria-pressed="false">童话</button><button type="button" data-filter="art" aria-pressed="false">官方绘图</button></div></div><p class="gallery-count" id="gallery-count" aria-live="polite">{len(data['gallery'])} 幅画面</p><div class="gallery-grid">{gallery}</div><p class="gallery-note">点开画面，可放大查看并找到原始出处。</p></div></section>

    <section class="closing page-width"><p lang="ja">リズと青い鳥</p><strong>把未说出口的，留在旋律里。</strong></section>
  </main>
  <footer class="liz-footer page-width"><a class="companion-link" href="../">回到玉子的商店街</a><details class="sources"><summary>作品与素材来源</summary><div><p>角色与原作画面属于作品权利方；官方素材的出处也可在画廊大图中查看。声画随记为页面的观看解读。</p><ul>{sources}</ul></div></details><p>{e(film['copyright'])}</p></footer>
  <dialog id="lightbox" class="lightbox" aria-labelledby="lightbox-title"><button class="lightbox-close" type="button" aria-label="关闭大图">×</button><div class="lightbox-stage"><button class="lightbox-prev" type="button" aria-label="上一张">‹</button><img id="lightbox-image" alt=""><button class="lightbox-next" type="button" aria-label="下一张">›</button></div><div class="lightbox-info"><p id="lightbox-credit"></p><h2 id="lightbox-title"></h2><p id="lightbox-caption"></p><span id="lightbox-count"></span></div></dialog>
</body>
</html>
'''
output = ROOT / 'liz' / 'index.html'
output.parent.mkdir(exist_ok=True)
output.write_text(html, encoding='utf-8', newline='\n')
print(f'Liz page built: {len(data["characters"])} characters, {len(data["gallery"])} gallery images.')
