"""Build the checked-in static homepage from its reviewed content and image ledger."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'tamako'
content = json.loads((ASSETS / 'content.json').read_text(encoding='utf-8'))


def e(value):
    return escape(str(value), quote=True)


def image(file, alt, cls='', eager=False):
    from PIL import Image
    with Image.open(ASSETS / file) as picture:
        width, height = picture.size
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="{e(cls)}" src="assets/tamako/{e(file)}" alt="{e(alt)}" width="{width}" height="{height}" {loading}>'


def heading(number, kicker, title, description=''):
    return f'<div class="section-head"><span class="section-no" aria-hidden="true">{number}</span><p class="section-kicker">{kicker}</p><h2>{title}</h2>' + (f'<p>{description}</p>' if description else '') + '</div>'


def link(url, label, cls='text-link'):
    return f'<a class="{cls}" href="{e(url)}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span></a>'


profile = content['profile']
facts = ''.join(f'<div><dt>{e(f["label"])}</dt><dd>{e(f["value"])}</dd></div>' for f in profile['facts'])
friends = ''.join(f'''<article class="friend-card"><div class="friend-portrait">{image('official/character-' + person['key'] + '.png', person['name'] + '官方角色立绘')}</div><span class="friend-relation">{e(person['relation'])}</span><h3>{e(person['name'])}</h3><p>{e(person['description'])}</p></article>''' for person in content['friends'])
places = ''.join(f'<article><span class="place-number">0{i}</span><div><h3>{e(place["name"])}</h3><p>{e(place["description"])}</p></div></article>' for i, place in enumerate(content['places'], 1))
episodes = ''.join(f'''<details class="episode-card"><summary><span class="episode-image">{image(episode['file'], '第' + str(episode['number']) + '集官方剧照')}</span><span class="episode-num">EP. {episode['number']:02}</span><span class="episode-title">{e(episode['title'])}</span><span class="episode-plus" aria-hidden="true">＋</span></summary><div class="episode-body"><p class="episode-ja" lang="ja">{e(episode['jaTitle'])}</p><p>{e(episode['description'])}</p>{link(episode['source'], '本集介绍')}</div></details>''' for episode in content['episodes'])
tracks = ''.join(f'''<a class="track" href="{e(track['url'])}" target="_blank" rel="noopener noreferrer"><span class="track-type">{e(track['type'])}</span><div><strong lang="ja">{e(track['title'])}</strong><small>{e(track['artist'])}</small></div><span class="track-arrow" aria-hidden="true">↗</span></a>''' for track in content['music'])

gallery_data = content['gallery']
gallery = ''.join(f'''<button class="gallery-item {'gallery-art' if item['category'] == 'art' else ''}" type="button" data-category="{e(item['category'])}" data-title="{e(item['title'])}" data-caption="{e(item['caption'])}" data-credit="{e(item['credit'])}" data-source="{e(item['source'])}" aria-label="放大：{e(item['title'])}">{image(item['file'], item['alt'])}<span class="gallery-overlay"><span class="gallery-category">{e(item['label'])}</span><strong>{e(item['title'])}</strong><span class="zoom-mark" aria-hidden="true">↗</span></span></button>''' for item in gallery_data)
sources = ''.join(f'<li>{link(source["url"], e(source["title"]))}</li>' for source in content['sources'])
staff = content['staff']

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#fff9f1">
  <meta name="description" content="认识北白川玉子，走进兔子山商店街。收藏玉子市场与玉子爱情故事的角色、剧集、音乐和原作瞬间。">
  <title>北白川玉子｜把每天，做成一点甜。</title>
  <link rel="icon" href="assets/tamako/mochi.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/tamako/style.css">
  <link rel="preload" as="image" href="assets/tamako/official/movie-visual.jpg" fetchpriority="high">
  <script src="assets/tamako/app.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">跳到正文</a>
  <header class="site-header"><div class="header-inner">
    <a class="brand" href="#home" aria-label="北白川玉子，回到首页"><img src="assets/tamako/mochi.svg" alt="" width="34" height="36"><span>北白川玉子<small>KITASHIRAKAWA TAMAKO</small></span></a>
    <button class="menu-toggle" type="button" aria-label="打开导航" aria-expanded="false" aria-controls="site-nav"><span></span><span></span></button>
    <nav id="site-nav" class="site-nav" aria-label="主导航"><a href="#about">关于玉子</a><a href="#friends">身边的大家</a><a href="#street">商店街</a><a href="#stories">作品与故事</a><a href="#gallery">画廊</a></nav>
    <span class="header-note" lang="ja">もちもち、しあわせ。</span>
  </div></header>
  <main id="main">
    <section class="hero" id="home" aria-labelledby="hero-title"><div class="section-shell hero-layout">
      <div class="hero-copy"><p class="eyebrow">TAMAKO'S LITTLE WORLD <span aria-hidden="true">✳</span></p><h1 id="hero-title">北白川玉子<span lang="ja">北白川たまこ</span></h1><p class="hero-tagline">把每天，做成一点甜。</p><p class="hero-description">从一间年糕店，到一整条商店街。<br>有朋友，有家人，还有慢慢说出口的心意。</p><div class="hero-actions"><a class="button button-pink" href="#about">认识玉子 <span aria-hidden="true">→</span></a><a class="button button-outline" href="#stories">走进她的故事 <span aria-hidden="true">→</span></a></div><div class="hero-meta"><span>京都动画</span><span>2013 · TV ANIMATION</span><span>2014 · LOVE STORY</span></div></div>
      <div class="hero-collage"><figure class="hero-main">{image('official/movie-visual.jpg', '玉子与饼藏走在春日树影下，玉子爱情故事官方主视觉', eager=True)}</figure><figure class="hero-inset">{image('official/episode-05.jpg', '玉子和朋友们的夏日日常，玉子市场第5集剧照')}<figcaption>一帧日常，一点心动。</figcaption></figure><div class="hero-stamp" aria-hidden="true">たまこ<br><span>まーけっと</span></div><p class="hero-caption">THE SMALL THINGS WE TREASURE <span>01 / 日常与青春</span></p></div>
    </div></section>
    <nav class="chapter-nav section-shell" aria-label="专题章节"><a href="#friends"><span class="chapter-number">01</span><div><small>PEOPLE</small><strong>一起长大的大家</strong></div><span class="chapter-arrow">↗</span></a><a href="#street"><span class="chapter-number">02</span><div><small>PLACES</small><strong>熟悉的商店街</strong></div><span class="chapter-arrow">↗</span></a><a href="#stories"><span class="chapter-number">03</span><div><small>STORIES</small><strong>从日常走向青春</strong></div><span class="chapter-arrow">↗</span></a></nav>

    <section class="section-shell section-pad about" id="about">
      {heading('01', 'HELLO, TAMAKO', '先从这个喜欢年糕的女孩说起。', '开朗、认真，又偶尔有一点迟钝。她让熟悉的小地方，变得格外可爱。')}
      <div class="profile-grid"><div class="profile-art">{image('official/character-tamako.png', '北白川玉子官方角色立绘')}<div class="profile-name"><small lang="ja">北白川たまこ</small><strong>北白川玉子</strong></div></div><div class="profile-copy"><h3>玉屋的女儿，<br>也是商店街的好邻居。</h3>{''.join('<p>' + e(paragraph) + '</p>' for paragraph in profile['description'])}<dl class="profile-facts">{facts}</dl><p class="profile-note">{e(profile['note'])}</p></div></div>
    </section>

    <section class="friends section-pad" id="friends"><div class="section-shell">
      {heading('02', 'THE PEOPLE AROUND HER', '和大家一起长大的日常。', '对门的青梅竹马、学校里的朋友、家人，还有那位意外来客。')}
      <div class="friends-grid">{friends}</div>
    </div></section>

    <section class="section-shell section-pad street" id="street">
      {heading('03', 'WELCOME TO USAGIYAMA', '转过街角，就是兔子山。', '年糕、花香、唱片与一声声招呼，组成了她最熟悉的风景。')}
      <div class="street-layout"><figure class="street-picture">{image('official/place-entrance.jpg', '兔子山商店街官方场景图')}<figcaption><span lang="ja">うさぎ山商店街</span> / 故事开始的地方</figcaption></figure><div class="street-copy"><p class="lead">从玉屋走到唱片店，<br>每一扇门后，都有人认识玉子。</p><div class="place-list">{places}</div></div></div>
      <div class="street-strip"><figure>{image('official/place-tamaya.jpg', '玉子家起居室的官方场景设定线稿')}<figcaption>玉屋的起居室 · 场景设定</figcaption></figure><figure>{image('official/place-florist.jpg', '花店官方场景')}<figcaption>花香经过的街角</figcaption></figure><figure>{image('official/place-record-shop.jpg', '唱片咖啡店官方场景')}<figcaption>一杯咖啡，一张唱片</figcaption></figure></div>
    </section>

    <section class="stories section-pad" id="stories"><div class="section-shell">
      {heading('04', 'EVERYDAY / LOVE STORY', '同一条街，两种心情。', '先认识她的日常，再听见她的心意。')}
      <div class="work-grid"><article class="work-card tv"><div class="work-visual">{image('official/hero-background.jpg', '玉子市场官方作品主视觉')}</div><div class="work-body"><div class="work-meta"><span>2013</span><span>TV ANIMATION · 12 EPISODES</span></div><h3>玉子市场<small lang="ja">たまこまーけっと</small></h3><p>{e(content['works']['tv']['description'])}</p><dl class="work-facts"><div><dt>关键词</dt><dd>商店街 / 朋友 / 四季</dd></div><div><dt>从这里开始</dt><dd>认识玉子和大家的日常</dd></div></dl><div class="work-links"><a class="text-link" href="#episodes">翻开 12 集日常 <span aria-hidden="true">↓</span></a>{link('https://tamakomarket.com/', '作品官网')}</div></div></article><article class="work-card movie"><div class="work-visual">{image('official/movie-visual.jpg', '玉子爱情故事官方作品主视觉')}</div><div class="work-body"><div class="work-meta"><span>2014.04.26</span><span>ANIMATION FILM</span></div><h3>玉子爱情故事<small lang="ja">たまこラブストーリー</small></h3><p>{e(content['works']['movie']['description'])}</p><dl class="work-facts"><div><dt>关键词</dt><dd>成长 / 未来 / 传达心意</dd></div><div><dt>观看顺序</dt><dd>TV 动画之后，再走进电影</dd></div></dl><div class="work-links">{link('https://tamakolovestory.com/trailer/', '官方预告')}{link('https://tamakolovestory.com/', '作品官网')}</div></div></article></div>
      <div class="film-moments"><figure>{image('official/movie-glasses.jpg', content['movieMoments'][0]['alt'])}<figcaption><small>01 / AT HOME</small>{e(content['movieMoments'][0]['caption'])}</figcaption></figure><figure>{image('official/movie-classroom.jpg', content['movieMoments'][1]['alt'])}<figcaption><small>02 / TOGETHER</small>{e(content['movieMoments'][1]['caption'])}</figcaption></figure><figure>{image('official/movie-riverbank.jpg', content['movieMoments'][2]['alt'])}<figcaption><small>03 / A LITTLE FURTHER</small>{e(content['movieMoments'][2]['caption'])}</figcaption></figure></div><p class="watch-note">从商店街的热闹，到独处时的安静。换了心情，还是我们熟悉的玉子。</p>
    </div></section>

    <section class="section-shell section-pad episodes" id="episodes">
      {heading('05', 'TWELVE LITTLE CHAPTERS', '一年四季，十二段日常。', '点开一集，看看那一天发生了什么。中文集名为参考译名。')}
      <div class="episode-grid">{episodes}</div>
    </section>

    <section class="music section-pad" id="music"><div class="section-shell">
      {heading('06', 'THE SOUND OF TAMAKO', '有些旋律，一听就想起她。')}
      <div class="music-layout"><div class="music-intro"><h3>从轻快的日常，<br>到青春的心跳。</h3><p>把熟悉的开场、片尾和电影主题曲放在一起，故事仿佛又从第一天开始了。</p><p class="music-hint">点击曲目，查看官方唱片介绍。</p></div><div class="music-tracks">{tracks}</div></div><p class="staff-note"><span>STAFF</span> 监督 · {e(staff['director'])}　/　系列构成・脚本 · {e(staff['writer'])}　/　角色设计 · {e(staff['characterDesign'])}<br>音乐 · {e(staff['music'])}　/　动画制作 · {e(staff['animation'])}</p>
    </div></section>

    <section class="section-shell section-pad gallery" id="gallery">
      <div class="gallery-heading">{heading('07', 'FRAMES TO KEEP', '收藏原作里的小小瞬间。', '笑容、放学路、朋友与春天。把故事中的画面，慢慢看清楚。')}<div class="gallery-filters" role="group" aria-label="画廊分类"><button type="button" class="is-active" data-filter="all" aria-pressed="true">全部</button><button type="button" data-filter="tv" aria-pressed="false">商店街日常</button><button type="button" data-filter="movie" aria-pressed="false">青春心事</button><button type="button" data-filter="art" aria-pressed="false">官方绘图</button></div></div><p class="gallery-count" id="gallery-count" aria-live="polite">{len(gallery_data)} 幅画面</p><div class="gallery-grid">{gallery}</div><p class="gallery-footnote">画廊采用官方绘图与原作截图。点开可放大，并查看画面的出处。</p>
    </section>

    <section class="closing section-shell"><p lang="ja">いつもの街、いつもの笑顔。</p><strong>明天，也来商店街吧。</strong><div class="closing-links"><a href="#home">回到故事的开始 ↑</a>{link('https://tamakomarket.com/', '玉子市场官网')}{link('https://tamakolovestory.com/', '玉子爱情故事官网')}</div></section>
  </main>
  <footer class="site-footer section-shell"><div><a class="footer-brand" href="#home">北白川玉子</a><p>© 京都アニメーション／うさぎ山商店街</p></div><details class="source-details"><summary>作品与素材来源</summary><div><p>角色、绘图与画面属于原作品权利方；图片出处可在画廊大图中查看。</p><ul>{sources}</ul></div></details><a class="back-top" href="#home" aria-label="回到顶部">↑</a></footer>
  <dialog class="lightbox" id="lightbox" aria-labelledby="lightbox-title"><button class="lightbox-close" type="button" aria-label="关闭大图">×</button><div class="lightbox-image-wrap"><button class="lightbox-prev" type="button" aria-label="上一张">‹</button><img id="lightbox-image" alt=""><button class="lightbox-next" type="button" aria-label="下一张">›</button></div><div class="lightbox-info"><div><p id="lightbox-credit"></p><h2 id="lightbox-title"></h2><p id="lightbox-caption"></p></div><span id="lightbox-counter"></span></div></dialog>
</body>
</html>
'''
(ROOT / 'index.html').write_text(html, encoding='utf-8', newline='\n')
print(f'Homepage built: {len(content["friends"])} relationships, {len(content["places"])} places, {len(content["episodes"])} episodes, {len(gallery_data)} gallery images.')
