---
title: 阿里云centos6搭建jenkins
tags: [jenkins,cent os]
date: 2020-3-22 20:15:14
---



#### 进入服务器，下载jenkins并安装

<!--more-->

[官方源](https://pkg.jenkins.io/redhat-stable/)用着实在是太慢了，这里我们使用清华大学的[开源镜像站](https://mirrors.tuna.tsinghua.edu.cn/jenkins/redhat/)，选择一个版本，服务器中输入`wget 版本链接`，

输入`rpm -ivh 文件`进行安装，`vim /etc/sysconfig/jenkins `修改端口以免冲突;

输入`which java`查看jdk地址，修改jenkins配置，`vim /etc/init.d/jenkins`

![jenkins-java](https://cdn.jsdelivr.net/gh/v-hiker/pic_repository/img/jenkins-java.png)

先`service jenkins start`，在浏览器打开ip:端口让jenkins加载必要的文件。

{% note warning%}

*下面部分如不更改，由于不通互联网，插件将很难成功下载*

{% endnote %}

输入`vi /var/lib/jenkins/updates/default.json `后参照[Jenkins安装插件提速](https://www.cnblogs.com/hellxz/p/jenkins_install_plugins_faster.html)进行修改，

```bash
:1,$s/http:\/\/updates.jenkins-ci.org\/download/https:\/\/mirrors.tuna.tsinghua.edu.cn\/jenkins/g
```

```bash
:1,$s/http:\/\/www.google.com/https:\/\/www.baidu.com/g
```

或者进入目录下，在终端直接输入

```bash
sed -i 's/http:\/\/updates.jenkins-ci.org\/download/https:\/\/mirrors.tuna.tsinghua.edu.cn\/jenkins/g' default.json && sed -i 's/http:\/\/www.google.com/https:\/\/www.baidu.com/g' default.json
```

接下来`service jenkins restart`启动，进入ip:端口，你将看见jenkins启动中。

按照提示查看密码并输入：

`cat /var/lib/jenkins/secrets/initialAdminPassword`

然后安装推荐的插件，等待安装完成。

成功进入jenkins界面后，依次点击Manage Jenkins-Manage Plugins-Advanced，拉到最下面，将默认的

更改为`https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json`,这可以加快获取列表的速度。

#### 配置jenkins所需插件

检查是否已安装以下两个插件：

1.Maven Integration 使我们可以开始一个maven项目作为任务

2.Git plugin 使我们可以读取存放在git仓库的项目

如果没有，就去插件管理里面搜索安装。

#### 配置jenkins全局工具

系统管理 --> 全局工具配置

![](https://cdn.jsdelivr.net/gh/v-hiker/pic_repository/img/20200424210313.png)

主要是配置jdk和git的地址，`which java`和`which git`查看就行了。

#### 新建任务

##### maven项目

![](https://cdn.jsdelivr.net/gh/v-hiker/pic_repository/img/20200424210813.png)

点击“新建任务”，输入名称，选择构建maven项目。

如图，添加源码位置，这里可以添加Credentials，一般使用https的方式添加源码就行了。使用ssh还需要到服务器里生成公钥添加到git。

![](https://cdn.jsdelivr.net/gh/v-hiker/pic_repository/img/20200424210947.png)

接下来添加build goal，`clean package -Dmaven.test.skip=true`这个是用来生成拥有Spring启动程序的项目的代码，如果是用来生成api供自己的程序使用，需要用`clean install -Dmaven.test.skip=true`这个命令。

![](https://cdn.jsdelivr.net/gh/v-hiker/pic_repository/img/image-20200424211711910.png)

最后添加Post Steps

选中`Run only if build succeeds`,add post-build step选择执行shell，按照如下格式：

```shell
#!/bin/bash 

#export BUILD_ID=dontKillMe这一句很重要，这样指定了，项目启动之后才不会被Jenkins杀掉。
export BUILD_ID=dontKillMe


#指定最后编译好的jar存放的位置
www_path=/usr/jars
#Jenkins中编译好的jar位置,其中md_metadata是自己的项目名称
jar_path=/var/lib/jenkins/workspace/md_metadata/target/

#Jenkins中编译好的jar名称，注意改成自己的项目名称
jar_name=metadata-0.0.1-SNAPSHOT.jar

#获取运行编译好的进程ID，便于我们在重新部署项目的时候先杀掉以前的进程，注意改成自己的项目名称
pid=`ps -ef | grep metadata-0.0.1-SNAPSHOT.jar | grep -v grep | awk '{print $2}'`
if [ -n "$pid" ]
then
   kill -9 $pid
fi

#进入指定的编译好的jar的位置
cd  ${jar_path}

#将编译好的jar复制到最后指定的位置
cp  ${jar_path}/${jar_name} ${www_path}

#进入最后指定存放jar的位置
cd  ${www_path}

#启动jar
java -jar ${jar_name} &

```

点击保存，ok。

##### 流水线任务

```shell
node{
    stage("starter"){
        echo "run starter"
        build job:"md_starter"
    }
    stage("eureka"){
        echo "run eureka"
        build job:"md_eureka"
    }
}
```

