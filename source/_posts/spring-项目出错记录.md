---
title: spring 项目出错记录
tags:
  - spring
  - maven
  - idea
reward_settings:
  enable: true
abbrlink: 7761f6cf
date: 2019-09-23 23:17:58
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

1、settings->editor->code style->default options->勾选wrap on typing

2、settings->editor->code style->java->wrapping and braces栏->ensure right margin is not exceeded

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

##### [引用自定义包报错The POM for xxxx is missing, no dependency information available](https://blog.csdn.net/qq_39150374/article/details/91969186)

打成springboot jar包,再引用自己做的包时，不要用这个打包命令:
`mvn package -Dmaven.test.skip=true`

正确的打包命令:
`mvn clean install -Dmaven.test.skip=true`

##### [关于SpringCloud（Nacos注册中心）集成Gateway时，路由跳转出错的解决方法](https://blog.csdn.net/weixin_43259821/article/details/104481875)

错误提示：

```shell
An exception 'java.lang.BootstrapMethodError: java.lang.NoClassDefFoundError: reactor/netty/NettyPipeline$SendOptions' [enable DEBUG level for full stacktrace] was thrown by a user handler's exceptionCaught() method while handling the following exception:
```

原因：springboot和gateway的版本不匹配

我是在集成eureka的时候出现的这个错误，看了这篇文章后检查自己的发现springboot版本为2.2.6，gateway的版本却为2.1.4，我去搜了一下[版本](https://spring.io/projects/spring-cloud-gateway#learn)才发现最新的是2.2.2了，因为我一直用idea提示的版本，结果造成了这种问题。

##### Failed to bind properties under 'spring.redis.port' to int:

```shell
Description:

Failed to bind properties under 'spring.redis.port' to int:

    Property: spring.redis.port
    Value: ${redis.defult.port}
    Origin: class path resource [application.yml]:12:11
    Reason: failed to convert java.lang.String to int

Action:

Update your application's configuration
```

仔细检查，可以发现我把default打成了defult，所以，引用云端配置的时候最好还是直接复制吧。

##### mysql插入emoji报错

`Incorrect string value: '\xF0\x9F\x90\x96' for column`

原因：

一个ASCII字符占用1个字节，一个汉字占用3个字节；
MySql的utf8编码最多3个字节，算不上真正的utf8字符集。在MySql5.5.3的版本增加了utf8mb4编码集，专门用于兼容4个字节的unicode。在MySql中utf8mb4是utf8的超集，除了修改数据库的编码集为utf8mb4外不需要做其他的修改。

解决办法：[MySql使用utf8mb4](https://blog.csdn.net/KillerAwp/article/details/82356042)

第一步：检查版本
查询版本语句：

`select version();`

第二步：修改MySql配置文件
打开mysql配置文件mysql/my.cnf或mysql/my.ini, 并且添加如下内容：

```sql
[client]
default-character-set=utf8mb4

[mysql]
default-character-set=utf8mb4

[mysqld]
character-set-client-handshake=FALSE
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
init_connect='SET NAMES utf8mb4'
```

第三步：重启数据库
1、Windows请到服务管理界面重新启动MySql服务：services.msc

2、Linux请执行命令：/etc/init.d/mysql restart

第四步：检查数据库配置
执行查看数据库字符集命令：

`SHOW VARIABLES WHERE Variable_name LIKE 'character_set_%' OR Variable_name LIKE 'collation%';`

```sql
+--------------------------+--------------------+
| Variable_name                         | Value |
+--------------------------+--------------------+
|| character_set_client         | utf8mb4 
|| character_set_connection | utf8mb4 
|| character_set_database     | utf8mb4 
|| character_set_filesystem | binary 
|| character_set_results         | utf8mb4 
|| character_set_server         | utf8mb4 
|| character_set_system         | utf8 
|| collation_connection         | utf8mb4_unicode_ci 
|| collation_database             | utf8mb4_unicode_ci 
|| collation_server                 | utf8mb4_unicode_ci
+--------------------------+--------------------+
```

必须保证: 
`character_set_client/character_se_connection/character_set_database/character_set_results/character_set_server`为`utf8mb4`。

第五步：更新客户端配置文件
```
jdbc.driverClassName=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/database?useUnicode=true&characterEncoding=utf8&autoReconnect=true&rewriteBatchedStatements=true
jdbc.username=username
jdbc.password=password
```

注意：jdbc.url的内容,`characterEncoding=utf8`可以配自动识别为utf8bm4  *//原作者的话，没理解*

第六步：修改数据库、表和列的字符集SQL语句：
```sql
ALTER DATABASE database_name CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE table_name table_name CHANGE column_name VARCHAR(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

第七步：修改应用连接字符串(druid)：
```java
<bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource" init-method="init" destroy-method="close">
    <property name="driverClassName" value="${jdbc-driver}"/>
    <property name="url" value="${jdbc-url}"/>
    <property name="username" value="${jdbc-user}"/>
    <property name="password" value="${jdbc-password}"/>
    <property name="filters" value="stat"/>
    <property name="maxActive" value="20"/>
    <property name="initialSize" value="1"/>
    <property name="maxWait" value="60000"/>
    <property name="minIdle" value="1"/>
    <property name="timeBetweenEvictionRunsMillis" value="3000"/>
    <property name="minEvictableIdleTimeMillis" value="300000"/>
    <property name="validationQuery" value="SELECT 'x'"/>
    <property name="testWhileIdle" value="true"/>
    <property name="testOnBorrow" value="false"/>
    <property name="testOnReturn" value="false"/>
    <property name="poolPreparedStatements" value="true"/>
    <property name="maxPoolPreparedStatementPerConnectionSize" value="20"/>
    <property name="connectionInitSqls" value="set names utf8mb4;"/>  //必须添加
</bean>
```
注意：mysql-connector-java驱动在5.1.13之前是不支持utf8mb4，请使用5.1.13以后的版本。