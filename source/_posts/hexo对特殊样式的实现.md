---
title: hexo对特殊样式的实现
tags: [hexo, next]
date: 2020-02-20 17:10:33
---

参考https://theme-next.org/docs/tag-plugins

<!--more-->

### Centered Quote

#### Usage

```javascript
center-quote.js
{% centerquote %}Something{% endcenterquote %}
<!-- Tag Alias -->
{% cq %}Something{% endcq %}
```

#### Examples

 {% cq %}

#### **赠人玫瑰，手有余香**

{% endcq %}

### Note

#### Usage

```javascript
note.js
{% note [class] [no-icon] %}
Any content (support inline tags too.io).
{% endnote %}

[class]   : default | primary | success | info | warning | danger.
[no-icon] : Disable icon in note.

All parameters are optional.
```

#### Examples

{% note warning%}

##### **虚怀若谷**

{% endnote %}

### Tabs

#### Usage

```javascript
tabs.js
{% tabs Unique name, [index] %}
<!-- tab [Tab caption] [@icon] -->
Any content (support inline tags too).
<!-- endtab -->
{% endtabs %}

Unique name   : Unique name of tabs block tag without comma.
                Will be used in #id's as prefix for each tab with their index numbers.
                If there are whitespaces in name, for generate #id all whitespaces will replaced by dashes.
                Only for current url of post/page must be unique!
[index]       : Index number of active tab.
                If not specified, first tab (1) will be selected.
                If index is -1, no tab will be selected. It's will be something like spoiler.
                Optional parameter.
[Tab caption] : Caption of current tab.
                If not caption specified, unique name with tab index suffix will be used as caption of tab.
                If not caption specified, but specified icon, caption will empty.
                Optional parameter.
[@icon]       : FontAwesome icon name (without 'fa-' at the begining).
                Can be specified with or without space; e.g. 'Tab caption @icon' similar to 'Tab caption@icon'.
                Optional parameter.
```

#### Examples

```javascript
{% tabs unique name %}
<!-- tab 第一重 -->
**昨夜西风凋碧树。独上高楼，望尽天涯路。**
<!-- endtab -->

<!-- tab 第二重 -->
**衣带渐宽终不悔，为伊消得人憔悴。**
<!-- endtab -->

<!-- tab 第三重 -->
**众里寻他千百度。蓦然回首，那人却在灯火阑珊处。**
<!-- endtab -->
{% endtabs %}
```
{% tabs unique name %}
<!-- tab 第一重 -->
**昨夜西风凋碧树。独上高楼，望尽天涯路。**
<!-- endtab -->

<!-- tab 第二重 -->
**衣带渐宽终不悔，为伊消得人憔悴。**
<!-- endtab -->

<!-- tab 第三重 -->
**众里寻他千百度。蓦然回首，那人却在灯火阑珊处。**
<!-- endtab -->
{% endtabs %}

### PDF

#### Usage

```javascript
{% pdf url [height] %}

[url]    : Relative path to PDF file.
[height] : Optional. Height of the PDF display element, e.g. 800px.
```

#### Examples

暂时没有


### Video

#### Usage

```javascript
{% video https://example.com/sample.mp4 %}
```


```javascript
{% video /path/to/your/video.mp4 %}
```
#### Examples

{% video https://cdn.jsdelivr.net/gh/v-hiker/pic_repository@master/%E9%A3%9E%E9%B8%9F.mp4 %}

自己找存储还是太麻烦了，不如随便找个视频网站上传，引用iframe什么的方便。

<iframe src="//player.bilibili.com/player.html?aid=18880837&cid=30791741&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>

### Group Pictures

#### Usage

```javascript
{% grouppicture [group]-[layout] %}{% endgrouppicture %}
{% gp [group]-[layout] %}{% endgp %}

[group]  : Total number of pictures to add in the group.
[layout] : Default picture under the group to show.
```

#### Examples
```javascript
{% grouppicture 9-3 %}
  ![1.jfif](/images/group_images/1.jfif)
  ![2.jfif](/images/group_images/2.jfif)
  ![3.jfif](/images/group_images/3.jfif)
  ![4.jfif](/images/group_images/4.jfif)
  ![5.jfif](/images/group_images/5.jfif)
  ![6.jfif](/images/group_images/6.jfif)
  ![7.jfif](/images/group_images/7.jfif)
  ![8.jfif](/images/group_images/8.jfif)
  ![9.jfif](/images/group_images/9.jfif)
{% endgrouppicture %}
```

{% grouppicture 9-3 %}
  ![1.jfif](/images/group_images/1.jfif)
  ![2.jfif](/images/group_images/2.jfif)
  ![3.jfif](/images/group_images/3.jfif)
  ![4.jfif](/images/group_images/4.jfif)
  ![5.jfif](/images/group_images/5.jfif)
  ![6.jfif](/images/group_images/6.jfif)
  ![7.jfif](/images/group_images/7.jfif)
  ![8.jfif](/images/group_images/8.jfif)
  ![9.jfif](/images/group_images/9.jfif)
{% endgrouppicture %}

这里没有显示全可能是我图片太大了，暂时也不知道怎么解决。