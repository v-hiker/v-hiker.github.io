---
title: Hexo使用
urlname: hexo-use
date: 2019-03-10 15:22:29
tags: [hexo,git]
---

## 备份

### 1.创建分支

直接github网页创建新分支hexo，找到“setting”-“Branches”，设置默认分支为“hexo”

<!--more-->

### 2.克隆仓库

克隆hexo分支至本地，将之前的Hexo文件夹中的
`_config.yml`，`themes/`，`source`，`scffolds/`，`package.json`，`.gitignore`复制到你克隆下来的仓库文件夹,删除主题文件夹中的.git文件夹，注意gitignore的内容

```
.DS_Store
Thumbs.db
db.json
*.log
node_modules/
public/
.deploy*/
```

### 3.提交代码

`git add .`，`git commit -m "备注"`，`git push origin Hexo`



## 恢复

### 1.下载git

下载地址：`https://www.git-scm.com/download/win`

一路默认选项安装

打开git bash

### 2.配置用户信息

```
$ git config --global user.name "v_hiker"
$ git config --global user.email "wangyanas@outlook.com"
```

如果用了 --global 选项，那么更改的配置文件就是位于你用户主目录下的那个，以后你所有的项目都会默认使用这里配置的用户信息。如果要在某个特定的项目中使用其他名字或者电邮，只要去掉 --global 选项重新配置即可，新的设定保存在当前项目的 .git/config 文件里。

要检查已有的配置信息，可以使用 `git config --list` 命令

### 3.配置SSH

输入`ssh-keygen -t rsa -C "wangyanas@outlook.com"`

路径选择默认，输入密码，回车,`C:\Users\wangy\.ssh`这个路径下会生成两个文件：id_rsa和id_rsa.pub

网页进入github，找到“Settings”-“SSH and GPG keys”-“New SSH key”，添加id_rsa.pub中的内容

### 4.安装npm

直接下载Node.js即可，地址：`https://nodejs.org/en/`

安装完成输入npm有正常命令提示即安装完成

### 5.初始化仓库

`npm install hexo-cli -g`、`npm install`、`npm install hexo-deployer-git`

### 备注

一、安装好git第一次执行hexo d可能出现的问题：

```
The authenticity of host 'github.com (52.74.223.119)' can't be established.
RSA key fingerprint is SHA256:-----------------------------------------.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

这个时候输入yes并回车，就会在.ssh文件生成known_hosts，即可正常使用

二、每次执行hexo 的都会提示输入密钥的密码`Enter passphrase for key '/c/Users/wangy/.ssh/id_rsa':`，解决办法为：

1.`ssh-agent bash`

2.`ssh-add -k /c/Users/wangy/.ssh/id_rsa`

2.输入密码回车，之后就好了



## hexo命令

hexo new "postName" #新建文章
hexo new page "pageName" #新建页面
hexo generate #生成静态页面至public目录
hexo server #开启预览访问端口（默认端口4000，'ctrl + c'关闭server）
hexo deploy #部署到GitHub
hexo help  # 查看帮助
hexo version  #查看Hexo的版本

删除文章直接本地删除md文件，然后执行hexo clean

使用时只需如 hexo g 一样写出首字母就行

hexo s -g #生成并本地预览
hexo d -g #生成并上传

设置文章摘要的长度:在合适的位置加上`<!--more-->`即可