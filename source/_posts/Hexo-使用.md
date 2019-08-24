---
title: Hexo 使用
date: 2019-03-10 15:22:29
tags: [hexo]
---

hexo new "postName" #新建文章
hexo new page "pageName" #新建页面
hexo generate #生成静态页面至public目录
hexo server #开启预览访问端口（默认端口4000，'ctrl + c'关闭server）
hexo deploy #部署到GitHub
hexo help  # 查看帮助
hexo version  #查看Hexo的版本

删除文章直接本地删除md文件，然后执行hexo clean

<!--more-->

使用时只需如 hexo g 一样写出首字母就行

hexo s -g #生成并本地预览
hexo d -g #生成并上传

设置文章摘要的长度:在合适的位置加上`<!--more-->`即可