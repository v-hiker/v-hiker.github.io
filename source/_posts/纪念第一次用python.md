---
title: 纪念第一次用python
urlname: first-use-of-python
date: 2019-03-18 23:12:13
tags: [python,Saito Asuka]
---
#### 用python3爬取百度贴吧图片

1 寻找想要爬取图片的网页，如http://tieba.baidu.com/p/6027318572
2 查看网页源代码

<!--more-->

![查看源代码.png](https://i.loli.net/2019/03/18/5c8fb640cbe4a.png)
3 放代码
```python
# coding:utf-8
import urllib.request
import re
import os

def get_html(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html
d = os.getcwd()
p = "\\pic"
isExists = os.path.exists(d+p)
if not isExists:
    os.mkdir(d+p)
    print("创建文件夹成功")
else:
    print("文件夹已存在")
    
imgName = 0

for i in range(3):
    
	html = get_html("http://tieba.baidu.com/p/6027318572?see_lz=1&pn="+str(i+1))
	html = html.decode('utf-8')
	
	reg = r'img class="BDE_Image" src="(.+?\.jpg)" size' 
	reg_img = re.compile(reg)
	imglist = re.findall(reg_img, html)
	
	
	for imgPath in imglist:
		print(imgPath)
		f = open("pic/"+str(imgName)+".jpg", 'wb')
		f.write((urllib.request.urlopen(imgPath)).read())
		f.close()
		imgName += 1
print(str(imgName)+" img have been saved in pic")
print("All Done!")

```

4 最终效果
![效果.png](https://i.loli.net/2019/03/18/5c8fb87a0f654.png)

附 半自动实现爬取图片，需要手输入链接及页数
```python
# coding:utf-8
import urllib.request
import re
import time

def mkdir():
    import os
    path = os.getcwd()
    LocalPath = input("Enter folder name to save pics(in now path): ");
    path = path+"\\"+LocalPath
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
        print (path+" 创建成功")
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+" 已存在")
    return LocalPath
LocalPath = mkdir()

def get_html(url):

    page = urllib.request.urlopen(url)
    html = page.read()
    return html

def get_url():
    url = input("输入想要获取源码的网页链接: ");
    url = url+'?see_lz='
    OrLz =  input("只看楼主？(0否/1是): ");
    OrLz = str(OrLz)
    url = url+OrLz
    print(url)
    return url
urlFirst = get_url()

page = input("输入页数:");
page = int(page)
imgName = 0
for i in range(page):
    url = urlFirst+'&pn='+str(i+1)
    print(url)
    html = get_html(url)
    html = html.decode('utf-8')
    
    reg = r'img class="BDE_Image" src="(.+?\.jpg)"' 
    reg_img = re.compile(reg)
    imglist = re.findall(reg_img, html)
    
    for imgPath in imglist:
        #print(imgPath)
        f = open(LocalPath+"/"+str(imgName)+".jpg", 'wb')
        f.write((urllib.request.urlopen(imgPath)).read())
        f.close()
        imgName += 1
        if(imgName%10 == 0):
            print(str(imgName)+" imgs have been saved in "+LocalPath)
    time.sleep(5)
print("All "+str(imgName)+" imgs have been saved in "+LocalPath)
```

问题: urllib.error.URLError: <urlopen error [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。
