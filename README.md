# 北白川玉子 · 今天，也有一点甜。

温暖的奶油白与樱粉角色宣传页，包含角色介绍、两部作品、六张画廊图片，以及三张眼镜玉子主题插画。

## 访问与部署

- 根首页：原生 HTML、CSS 与 JavaScript，无构建或运行时依赖。
- GitHub Pages：继续使用原仓库的 CNAME；.nojekyll 保证静态文件直接发布。
- 本地查看：在仓库目录执行 `python -m http.server 8766 --bind 127.0.0.1`，浏览器打开本地服务。
- 旧博客保留在 `/blog/`，主宣传页没有博客入口；原文章 URL 与资源也保留。
- 主页面不显示域名字样或“非官方同好站”标签。

## 交互与修改入口

- `index.html`：页面文案、导航、角色信息和画廊条目。
- `assets/tamako/style.css`：电脑和手机布局、配色与字体。
- `assets/tamako/app.js`：手机导航、画廊分类、大图查看及键盘操作。
- 画廊支持分类筛选、点击放大、上一张/下一张、方向键和 Escape 关闭。
- 尊重系统的减少动态效果设置；主要图片在本地，非首屏图片懒加载。

## 素材来源

角色与作品为《玉子市场》《玉子爱情故事》，资料参考作品官方站。

- https://tamakomarket.com/character/1/
- https://tamakolovestory.com/character/
- https://tamakomarket.com/story/
- https://tamakolovestory.com/introduction/

官方图片的来源与原始尺寸在 `assets/tamako/official-sources.json`。原始作品图片保持原有版权信息。

`hero-market.png` 和三张 `glasses-*.png` 是根据角色参考生成的主题插画，并非电影截图。提示词及来源分别在 `hero-prompts.json`、`glasses-prompts.json`。眼镜造型的本地绘图参考来自电影镜头转载，未将转载图作为网页图片发布。

## 博客保留

`scripts/migrate-blog.py` 从迁移前的固定 Git 提交生成 `/blog/` 副本，重写站内路径并使用本地 KEEP 资源。不要从已改版的主首页重新提取博客。

`scripts/blog-migration-report.json` 保存迁移核对结果。新增博客副本保留 11 篇文章、搜索索引及分页；原始文章文件保持可访问。
