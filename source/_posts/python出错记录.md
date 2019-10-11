---
title: python出错记录
date: 2019-10-09 21:14:40
urlname: python-error-record
tags: [python]
---

##### pycharm中升级pip出错，‘NoneType' object has no attribute 'bytes'

使用`easy_install -U pip`安装而不是`python -m pip install --upgrade pip`

##### Do you need to install a parser library?

`soup = BeautifulSoup(r.text, 'lxml')`更改为：

`soup = BeautifulSoup(r.text, 'html.parser')`