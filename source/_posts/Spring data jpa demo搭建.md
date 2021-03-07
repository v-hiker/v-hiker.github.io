---
title: Spring data jpa demo
date: 2021-03-06 23:17:58
tags: [spring boot,jpa]
reward_settings:
  enable: true
---

从开始接触Spring这一个框架开始使用的持久层框架就一直是mybatis，最近听说了还有另外的叫做jpa的框架，为了体验一下有什么区别，于是决定打一个小demo测试一下。

<!--more-->

## 相关工具准备

##### mysql

用以搭建本地数据库。

下载地址：[https://dev.mysql.com/downloads/installer/](https://dev.mysql.com/downloads/installer/ ) 

注意，有两个安装包，`mysql-installer-web-community-8.0.22.0.msi`和`mysql-installer-community-8.0.22.0.msi`,前者是安装之后再在线下载，后者为离线安装。

安装过程参照百度，通过msi方式安装完后mysql server默认打开，可以使用数据库连接工具进行测试。

创建一个数据库用于测试。

##### IDEA

一个很方便的ide。

##### Navicat

老牌数据库管理工具

## 开始

### 创建项目

idea新建Spring Initializr项目，选择`Lombok`,`Spring Data JPA`,`MySQL Driver`,`Spring Web`等相关依赖。

编写相关配置文件`application.properties`或者采用`.yml`格式，这里使用`.yml`格式：

```yaml
server:
  port: 9001
  servlet:
    context-path: /

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull&allowMultiQueries=true&useSSL=false
    username: jpa
    password: jpa1234
  jpa:
    database: mysql
    database-platform: org.hibernate.dialect.MySQL5InnoDBDialect
    show-sql: true
    hibernate:
      ddl-auto: update
```

### 创建实体类

```java
@Data
@Entity
@Table(name = "base_user")
public class User implements Serializable {
    /**
     * 主键，用户id
     */
    @Id
    @GenericGenerator(name = "idGenerator", strategy = "org.hibernate.id.UUIDGenerator")
    @GeneratedValue(generator = "idGenerator")
    private String userId;

    /**
     * 用户名
     */
    @Column(name = "user_name", unique = true, nullable = false, length = 64)
    private String userName;

    /**
     * 用户密码
     */
    @Column(name = "password", nullable = false, length = 128)
    private String password;

    /**
     * 用户邮箱
     */
    @Column(name = "email", nullable = false, length = 64)
    private String email;

}
```

> 主键采用UUID策略
>  `@GenericGenerator`是Hibernate提供的主键生成策略注解，注意下面的`@GeneratedValue`（JPA注解）使用generator = "idGenerator"引用了上面的name = "idGenerator"主键生成策略

> JPA自带的几种主键生成策略
>
> - TABLE： 使用一个特定的数据库表格来保存主键
> - SEQUENCE： 根据底层数据库的序列来生成主键，条件是数据库支持序列。这个值要与generator一起使用，generator 指定生成主键使用的生成器（可能是orcale中自己编写的序列）
> - IDENTITY： 主键由数据库自动生成（主要是支持自动增长的数据库，如mysql）
> - AUTO： 主键由程序控制，也是GenerationType的默认值

如果需要给表添加注释，需要使用`@Column(nullable = false,columnDefinition = "varchar(100) default '' comment '我是字段注释...'")`,这个时候`length`的值就不起作用了，因此使用`columnDefinition`时需要写全字段类型、长度等属性。

为了在数据库生成相应注释，这里采用`columnDefinition`的写法：

```java
@Data
@Entity
@Table(name = "base_user")
public class User implements Serializable {
    @Id
    @GenericGenerator(name = "idGenerator", strategy = "org.hibernate.id.UUIDGenerator")
    @GeneratedValue(generator = "idGenerator")
    private String userId;

    @Column(name = "user_name", unique = true, nullable = false, columnDefinition = "varchar(64) comment '用户名'")
    private String userName;

    @Column(name = "password", nullable = false, columnDefinition = "varchar(128) comment '用户密码'")
    private String password;

    @Column(name = "email", nullable = false, columnDefinition = "varchar(64) comment '用户邮箱'")
    private String email;

}
```

### 创建repository

```java
public interface UserRepository extends JpaRepository<User,String> {
}
```

### 启动项目

这时候启动项目，可以看见控制台输出相应的创建表语句

```sql
Hibernate: create table base_user (user_id varchar(255) not null, email varchar(64) comment '用户邮箱' not null, password varchar(128) comment '用户密码' not null, user_name varchar(64) comment '用户名' not null, primary key (user_id)) engine=InnoDB
```

通过navicat或者idea自带的连接工具查看数据库test，可以发现已经建立了`base_user`的表。

这个时候在实体类中添加一个字段

```java
@ApiModelProperty(value = "用户昵称")
@Column(name = "nick_name", nullable = false, columnDefinition = "varchar(64) comment '用户昵称'")
private String nickName;
```

重新启动项目，会发现控制台输出

```sql
Hibernate: alter table base_user add column nick_name varchar(64) comment '用户昵称' not null
```

## 测试

### 配置swagger

为了方便测试，采用swagger2来生成api文档，这里使用3.0.0版本，pom中只需要添加一项依赖即可：

```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-boot-starter</artifactId>
    <version>3.0.0</version>
</dependency>
```

配置类：

在3.0版本中，移除了`@EnableSwagger2`的注解，在应用类注解`@EnableOpenApi`即可加入swagger文档。为了实现一些自定义配置，还是可以写一个配置类。

```java
@Configuration
public class Swagger2Config {
    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.OAS_30)
                .apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.withMethodAnnotation(ApiOperation.class))
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("jpa测试接口文档")
                .description("采用swagger2 3.0版本")
                .contact(new Contact("xx", "#", "xx@qq.com"))
                .version("1.0")
                .build();
    }
}
```

### 添加controller

这里为了方便，直接将repository注入到controller中进行实现，省略了中间的service层。

```java
@EnableOpenApi
@Api(tags = "基础数据通用接口")
@RestController
@RequestMapping("/user")
public class UserController {
    @Resource
    private UserRepository userRepository;

    @ApiOperation(value = "新增用户", httpMethod = "POST", response = String.class)
    @PostMapping("/add")
    public String addUser(@RequestBody @Validated User user) {
        User result = userRepository.save(user);
        return result.getUserId();
    }

    @ApiOperation(value = "更新用户", httpMethod = "POST", response = String.class)
    @PostMapping("/update")
    public String updateUser(@RequestBody @Validated User user) {
        User result = userRepository.saveAndFlush(user);
        return result.getUserId();
    }

    @ApiOperation(value = "查询用户详情", httpMethod = "GET", response = User.class)
    @GetMapping("/detail")
    public User getUserDetail(@RequestParam(value = "userId") String userId) {
        Optional<User> user = userRepository.findById(userId);
        return user.orElse(null);
    }

    @ApiOperation(value = "查询用户列表", httpMethod = "GET", response = User.class)
    @GetMapping("/list")
    public List<User> getUserList() {
        List<User> userList = userRepository.findAll();
        return userList;
    }

    @ApiOperation(value = "删除用户", httpMethod = "DELETE", response = Boolean.class)
    @DeleteMapping("/detail")
    public Boolean deleteUser(@RequestParam(value = "userId") String userId) {
        userRepository.deleteById(userId);
        return Boolean.TRUE;
    }
}
```

启动项目，在浏览器中打开[http://localhost:9001/swagger-ui/#/](http://localhost:9001/swagger-ui/#/)即可看到API文档并进行测试了。



