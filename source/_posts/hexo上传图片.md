---
title: hexo上传图片
date: 2019-03-10 17:23:39
tags: [hexo,Saito Asuka]
---
#### 如何上传本地图片
1 把主页配置文件_config.yml 里的post_asset_folder:这个选项设置为true
2 在hexo目录下执行
    npm install hexo-asset-image --save
安装一个可以上传本地图片的插件
<!--more-->
3 等待一小段时间后，再运行hexo n "xxxx"来生成md博文时，/source/_posts文件夹内除了xxxx.md文件还会生成一个同名的文件夹
4 最后在xxxx.md中想引入图片时，先把图片复制到xxxx这个文件夹中，然后只需要在xxxx.md中按照markdown的格式引入图片：
`![你想输入的替代文字](xxxx/图片名.jpg)`
#### 如何上传在线图片
1 选择图床，如https://sm.ms/
2 上传图片后就能直接生成带有链接的图片
[![鸟2.jpg](https://i.loli.net/2019/03/18/5c8f7ed81bffd.jpg)](https://i.loli.net/2019/03/18/5c8f7ed81bffd.jpg)

代码为
```markdown
[![鸟2.jpg](https://i.loli.net/2019/03/18/5c8f7ed81bffd.jpg)](https://i.loli.net/2019/03/18/5c8f7ed81bffd.jpg)
```