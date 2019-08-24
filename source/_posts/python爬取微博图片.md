---
title: python爬取微博图片
date: 2019-03-20 22:52:33
tags: [python]
---

#### 代码来自
> 作者：cool_flag 
来源：CSDN 
原文：https://blog.csdn.net/cool_flag/article/details/78992628 

本来以为微博应该会跟百度贴吧一样简单，开始动手后才发现不是我想的那样，在百度搜索后找到了上面这篇帖子，受益匪浅。该作者使用的是微博移动版https://weibo.cn
其原话是
> 因为html5版的微博页面和web端一样也是采用动态加载的，什么是动态加载呢，就是你打开一页可以一直往下翻，他会一直帮你自动加载，直到底部。这就导致了代码是根据你的行为(鼠标的点击等等)不断变化的。

<!--more-->

> 接着第二个问题是模拟登陆，开始我想着是post模拟登陆输入用户账号和密码即可，后来发现是我想多了…好像有点困难，于是就采用了cookie直接登陆，这个方法简单粗暴。

##### 获取cookie方法
1 点击进入移动版微博https://weibo.cn
2 登陆
3 进入想要爬取图片的博主的主页，如https://weibo.cn/u/1856334535
4 谷歌浏览器F12打开调试窗口
5 刷新，点击第一个文件
![cookie-1.png](https://i.loli.net/2019/03/20/5c92619ef1239.png)
![cookie-2.png](https://i.loli.net/2019/03/20/5c92619e7f467.png)
6 向下寻找Request Headers，其中的cookie项一长串即为所需，复制下来
![cookie-3.png](https://i.loli.net/2019/03/20/5c92619ec5b21.png)


#### 遇到的问题

原作者有一段获取微博发送时间的代码
```python
        #获取微博发送时间
        hms = ' '.join(weibo_tag.find(
            'span', attrs={'class': 'ct'}).text.replace('\xa0', '').replace(':', '-').split(' ')[:2])
```
我一开始运行到这里就会报错，大致内容是找不到，然后经过排查是因为截取微博代码段的代码`weibo_tags_list = soup.find_all('div', attrs={'class': 'c'}, id=True)`有没考虑完全的情况，如微博https://weibo.cn/u/1856334535
其源代码经过查找后会有下面两种：
```xml
<div class="c" id="M_HlmjxqNMs">
	<div>
		<span class="ctt">GRL<br/>斋藤飞鸟X西野七濑 </span>
	</div>
	<div>
		<a href="https://weibo.cn/mblog/pic/HlmjxqNMs?rl=0">
			<img alt="图片" class="ib" src="http://wx2.sinaimg.cn/wap180/6ea56ac7ly1g15zu9yuunj20u011igqp.jpg"/>
		</a> <a href="https://weibo.cn/mblog/oripic?id=HlmjxqNMs&amp;u=6ea56ac7ly1g15zu9yuunj20u011igqp">原图</a> <br/>
		<a href="https://weibo.cn/attitude/HlmjxqNMs/add?uid=6070849388&amp;rl=0&amp;st=3622c9">赞[786]</a> <a href="https://weibo.cn/repost/HlmjxqNMs?uid=1856334535&amp;rl=0">转发[67]</a> <a class="cc" href="https://weibo.cn/comment/HlmjxqNMs?uid=1856334535&amp;rl=0#cmtfrm">评论[30]</a> <a href="https://weibo.cn/fav/addFav/HlmjxqNMs?rl=0&amp;st=3622c9">收藏</a>
		<!-- --> <span class="ct">03月17日 19:00 来自微博 weibo.com</span>
	</div>
</div>
```
```xml
<div class="c" id="M_HldFo0Vu8">
	<div>
		<span class="ctt">
			<img alt="[haha]" src="//h5.sinaimg.cn/m/emoticon/icon/others/h_haha-6934824adc.png" style="width:1em; height:1em;"/>
		</span>
	</div>
</div>
```
一开始我的想法是对find_all的条件增加限制，比如在原来的div标签中查找到`img alt="图片" class="ib"`，然而上网搜索了一段时间后还是不知道应该怎么写，最后我放弃了这种想法，转而思考在没有获取到正确的代码段时不获取时间。于是便有了下面的一段代码
```python
        if weibo_tag.find('span', text=re.compile('来自微博')):
            hms = ' '.join(weibo_tag.find(
                'span', attrs={'class': 'ct'}).text.replace('\xa0', ' ').replace(':', '-').split(' ')[:2])
        else:
            hms = "none"+"-"+str(page)+"-"+str(entry)
```
法子是笨了点，结果也导致最后文件夹里多了很多none-xx-xx的图片，但好歹是运行起来了。
#### 思考
在第一次爬取贴吧图片时网页获取我是用的urllib.request.urlopen(url)，结果运行时会出现错误
urllib.error.URLError: <urlopen error [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。
这次的代码里面使用的是requests.get(url, headers=headers)，然后一直运行也没有什么错误，不知道是因为不同方式还是因为这次请求连接使用了cookie的原因，今天时间不多了，便暂不思考，留待以后吧。

#### 附 最终代码
```python
import requests
from bs4 import BeautifulSoup as bs
import os
import re

#uid即进入对方微博主页后网址部分/u/后的那一串数字
uid = input('请输入所要爬取的用户id:')
url = 'https://weibo.cn/u/'+uid
cookie = input('请输入你的新浪微博的cookie:')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36', 'Cookie': cookie}

r = requests.get(url, headers=headers)
soup = bs(r.text, 'html.parser')
# 所访问的微博用户名
weibo_user_name = soup.find('title').text.replace('的微博', '')
# 存放图片的根目录
print(weibo_user_name)

rootDir = 'E://pic//' + weibo_user_name + '//'
# 微博总页数,通过审查元素可知
totalPage = int(soup.find('input', attrs={'name': 'mp'}).attrs['value'])
print('总共检测到%d页微博页面' % totalPage)
# 每页微博的URL的列表
weibo_urlList = [url + '?page=' + str(i + 1) for i in range(totalPage)]

#当前已爬取的图片总数
pictrue_num = 0
for page, weibo_url in enumerate(weibo_urlList):
    r = requests.get(weibo_url, headers=headers)
    soup = bs(r.text, 'html.parser')
    #每条微博所对应的标签代码块列表
    weibo_tags_list = soup.find_all('div', attrs={'class': 'c'}, id=True)
    #微博发送时间与微博配图的字典
    imgs_urls_dic = {}
    for entry, weibo_tag in enumerate(weibo_tags_list):
        print('正在爬取第%d页第%d条微博' % (page + 1, entry + 1))
        #获取微博发送时间
        if weibo_tag.find('span', text=re.compile('来自微博')):
            hms = ' '.join(weibo_tag.find(
                'span', attrs={'class': 'ct'}).text.replace('\xa0', ' ').replace(':', '-').split(' ')[:2])
        else:
            hms = "none"+"-"+str(page)+"-"+str(entry)
        #该条微博若带有组图，获取组图中所有图片的URL
        if weibo_tag.find('a', text=re.compile('组图')):
            imgs_url = weibo_tag.find('a', text=re.compile('组图')).attrs['href']
            html = requests.get(imgs_url, headers=headers)
            imgs_soup = bs(html.text, 'html.parser')
            imgs_tags_List = imgs_soup.find_all('img', alt='图片加载中...')
            img_urls_list = [imgs_tag.attrs['src'].replace(
                'thumb180', 'large') for imgs_tag in imgs_tags_List]
            imgs_urls_dic[hms] = img_urls_list
        #该条微博仅有一张配图，或者没有图片，获取图片的URL
        else:
            img_tags_List = weibo_tag.find_all('img', alt='图片')
            img_urls_list = [img_tag.attrs['src'].replace(
                'wap180', 'large') for img_tag in img_tags_List]
            imgs_urls_dic[hms] = img_urls_list
    print('第%d页微博爬取完毕,开始生成图片' % (page + 1))
    for hms, img_urls_list in imgs_urls_dic.items():
        for index, img_url in enumerate(img_urls_list):
            #生成图片的存放路径，图片被命名为微博发送时间
            path = rootDir + hms
            #如果一条微博在同一时间发送了多张图片(即组图)的命名处理
            if(index > 0):
                path = path + '(' + str(index) + ')'
            path = path + '.jpg'
            try:
                if not os.path.exists(rootDir):
                    #makedirs递归生成多级目录，mkdir仅能生成一级目录
                    os.makedirs(rootDir)
                if not os.path.exists(path):
                    r = requests.get(img_url)
                    with open(path, 'wb') as f:
                        f.write(r.content)
                        pictrue_num = pictrue_num + 1
                        print('success,成功爬取第%d张图片' % pictrue_num)
                else:
                    print('%s已经存在' % path)
            except:
                print('爬取失败,%s' % img_url)
print('总共爬取了%d张图片，存放在 %s 目录下' % (pictrue_num, rootDir))
```
