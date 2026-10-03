# 北白川玉子 · 把每天，做成一点甜。

奶油白与樱粉的角色／作品专题页，包含角色资料、六位人物关系、五个商店街场所、两部作品、十二集导览、音乐介绍和十二幅原作画廊。首屏使用官方主视觉拼贴；电影家居镜头自然融入日常图组。

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
- `assets/tamako/content.json`：经过来源核对的内容与画廊数据。
- `scripts/build-home.py`：从内容生成已提交的静态首页。仅修改内容后需要运行，生成时使用 Python 与 Pillow；部署无需构建。
- 画廊按日常、电影与官方绘图筛选，支持点击放大、上一张/下一张、方向键、Escape 关闭及图片出处链接。十二集导览使用原生可展开卡片。
- 尊重系统的减少动态效果设置；主要图片在本地，非首屏图片懒加载。

## 素材来源

角色与作品为《玉子市场》《玉子爱情故事》，资料参考作品官方站。

- https://tamakomarket.com/character/1/
- https://tamakolovestory.com/character/
- https://tamakomarket.com/story/
- https://tamakolovestory.com/introduction/

当前页面素材的来源、尺寸、类型与 SHA-256 在 `assets/tamako/official/manifest.json`。官方原图保留原有版权信息，没有生成插画混入画廊。

电影教室画面来自 TBS 节目目录，河岸画面来自 JFDB／UNIJAPAN 的电影宣传资料。家居眼镜镜头是已核实的电影画面转载，尚未定位官方上游帧；在素材记录和大图出处中明确标注，未冒充官方发布图。

早期方案的 `hero-market.png`、`glasses-*.png` 与相应提示词留作设计历史记录，当前主页不引用。`official-sources.json` 为初版的三图记录，当前版本以 `official/manifest.json` 为准。

## 博客保留

`scripts/migrate-blog.py` 从迁移前的固定 Git 提交生成 `/blog/` 副本，重写站内路径并使用本地 KEEP 资源。不要从已改版的主首页重新提取博客。

`scripts/blog-migration-report.json` 保存迁移核对结果。新增博客副本保留 11 篇文章、搜索索引及分页；原始文章文件保持可访问。
