---
title: spring 项目出错记录
date: 2019-09-23 23:17:58
urlname: spring-error-record
tags: [spring,maven,idea]
---

##### 新拉的项目下完依赖后dependencies还是出现红色波浪线

删除pom中相关依赖,import change后重新添加即可

<!--more-->

##### 启动类报错：

```
错误: 找不到或无法加载主类 XXXX
原因: java.lang.ClassNotFoundException: XXXX
```

`mvn clean install`或者使用lifecycle的clean&install即可

##### generatorConfig.xml中

`http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd`红色，使用idea的红色小灯泡，点击Fetch external resource即可解决

##### SprinfBoot启动eureka出现WARNING: 

`An illegal reflective access operation has occurred`

原因：jdk版本过高，（或许是spring5+的bug，未深究），解决办法：降低项目jdk至1.8以下

![imageTemp.png](https://i.loli.net/2019/09/29/Z1pnWJO8VgNfMmU.png)

如若依然不行，查看每个module中jdk版本是否已降低

![modulejdk.png](https://i.loli.net/2019/09/29/dgvwRuiUMXmK7Oa.png)

##### 启动服务报错：

`Caused by: java.nio.charset.MalformedInputException: Input length = 1`

编码设置有问题，File --> Settings --> Editor --->File Encodings   ，将所有的格式都转成utf-8格式

##### swagger`/swagger-resources/configuration/ui`报错404

![swagger-ui-404.png](https://i.loli.net/2019/09/29/OQR1gEbaZMTse6K.png)

查看网上问题后，去检查swagger-ui和swagger2的版本发现也是一样的，实在是没找出来毛病，于是先更改了一个小问题：

service右上角显示小红x，原因是因为之前更改了一次package的名称，导致configuration里面出现了一点问题，只需要右键编辑以下就好了

![right-red-x.png](https://i.loli.net/2019/09/29/qi5Y2muyJ9pABoG.png)
![x-next.png](https://i.loli.net/2019/09/29/b8WqjHUhsDx1Gvg.png)

在解决了这个事情后，我重启了服务，随便刷了一下swagger，发现它竟然好了！！！我佛了

##### idea2019.2中中文字体忽大忽小不规范的问题

File --> Settings --> Editor --->Font调整“Fallback font”为SimHei、SimSun、YouYuan等

##### idea2019.2及以上版本pom文件添加dependency不提示补全

据说是2019.2版本BUG，但是我更新2019.03后依然还是这样，准确地说是时灵时不灵，需要先输入groupID才会提示，可以参考isuue：https://youtrack.jetbrains.com/issue/IDEA-215097

##### [idea设置代码行宽度超出限制时自动换行](https://www.jianshu.com/p/8f71436e5bb1)

##### duplicate declaration of version

```
Some problems were encountered while building the effective model for tk.hiker.blog:starter:pom:0.0.1-SNAPSHOT
'dependencyManagement.dependencies.dependency.(groupId:artifactId:type:classifier)' must be unique: com.alibaba:fastjson:jar -> duplicate declaration of version 1.2.60 @ line 114, column 25
It is highly recommended to fix these problems because they threaten the stability of your build.
For this reason, future Maven versions might no longer support building such malformed projects.
```

单纯的因为多写了一遍依赖，仔细检查下pom文件应该就能找到

##### Content type '' not supported

因为我在不需要传值的方法中写了consumes

`@GetMapping(path = "/postsinfo/getallposts",consumes = "application/json;charset=UTF-8")`

##### MyBatis排序时使用order by 动态参数时需要注意，用$而不是#