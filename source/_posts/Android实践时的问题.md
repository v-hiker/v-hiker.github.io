---
title: Android实践时的问题
date: 2019-05-18 22:03:50
tags: [Android]
---
踩坑记；
<!--more-->
## WebView
### WebViewClient
> 1, 若没有设置 WebViewClient 则在点击链接之后由系统处理该 url，通常是使用浏览器打开或弹出浏览器选择对话框。
2, 若设置 WebViewClient 且该方法返回 true ，则说明由应用的代码处理该 url，WebView 不处理。
3, 若设置 WebViewClient 且该方法返回 false，则说明由 WebView
处理该 url，即用 WebView 加载该 url。

在网上搜索出来的在webview内打开url的方法如下：
```java
webview.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view,String url){
                    view.loadUrl(url);
                    return false;
                }
            }
        });
```

可看出该方法直接重写WebViewClient，return false使情况3达成，我一开始就这样直接照搬了，然后一下午我都一直在遇到`net::ERR_UNKNOWN_URL_SCHEME`这个错误，发生在某度搜索结果的各种跳转界面。
是夜，得到解决办法：
```java
webview.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view,String url){
                if(url.startsWith("http:") || url.startsWith("https:") ) {
                    view.loadUrl(url);
                    return false;
                }else{
					Intent intent2 = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                    startActivity(intent2);
                    return true;
                }
            }
        });
```
增加了一个判断，如果是非http(s)型，如百度微信电话邮件等跳转链接，则将其传递到能响应此链接的应用中，返回true，对应类型2。

我天真地以为这就是一切了，然后点击打不开的跳转页面，不报net错误了，第一次直接闪回主界面，第二次就整个程序崩溃了。
苦思，无果，遂寻一佬名fish，佬言待其catch一异常，然尚未及现log，页面竟已正常跳转，大惊，忙询佬其缘。
```java
webview.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view,String url){
                if(url.startsWith("http:") || url.startsWith("https:") ) {
                    view.loadUrl(url);
                    return false;
                }else{
                    try{
                        Intent intent2 = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                        startActivity(intent2);
                        return true;
                    }
                    catch (Exception ex){
                        Log.d("","TEST TEST:" + ex.getMessage());
                        return true;
                    }
                }
            }
        });
```
佬曰：如果存在可以打开链接的app，webview就会通过intent申请打开该应用，如果不存在，就会先报错不存在该应用然后提示下载该应用，我这代码没有处理报错，于是程序就直接卡在这一部崩溃而不进行下一步的下载界面跳转。
佬还曰：写函数必先catch e，对防止程序崩溃是极好的。
事毕，愧，记以纪之。

因为遇见了返回重定向的问题，又仔细检查了一遍，发现
```java
if(url.startsWith("http:") || url.startsWith("https:") ) {
                    view.loadUrl(url);
                    return false;}
```

这里应该直接return false就好了。
```java
webview.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view,String url){
                if(url.startsWith("http:") || url.startsWith("https:") ) {
                    return false;
                }else{
                    try{
                        Intent intent2 = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                        startActivity(intent2);
                        return true;
                    }
                    catch (Exception ex){
                        Log.d("","TEST TEST:" + ex.getMessage());
                        return true;
                    }
                }
            }
        });
```
应该是最终版了，希望是最终版了。
把匹配的判定改了一下
```java
webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, final String url) {
                if (("https".equalsIgnoreCase(Uri.parse(url).getScheme())) ||
                        ("http".equalsIgnoreCase(Uri.parse(url).getScheme()))) {
                    return false;
                } else {
                    try {
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                        startActivity(intent);
                        return true;
                    } catch (Exception ex) {
                        return true;
                    }
                }
            }
        });
```
### WebSettings
在[bilibili手机版网页](https://m.bilibili.com/index.html "bilibili手机版网页")点击视频后，会在一两秒内白屏，上网寻之，[webview中屏蔽bilibili启动客户端app的请求](https://blog.csdn.net/weixin_33772645/article/details/87316890 "webview中屏蔽bilibili启动客户端app的请求")，有同样的问题，然而经测试并没有什么用，查看控制台error，才发现"Uncaught TypeError: Cannot read property 'getItem' of null"这个错误提示，经过[搜索](http://www.codes51.com/article/detail_4140743.html "搜索")：
> 是因为该网页的js写得不规范(擦，原来是前端哥们挖的坑)：
在JS运行的时候你的页面还没有加载完成，所以你的JS代码找不到你的页面元素，就会抛出这个问题。
在网页端修改方法：把JS的引入文件，放在文档后面就可以避免了。
当然，在安卓端修改也只是一句话的事： webView.getSettings().setDomStorageEnabled(true);
就可以忽略这个问题执行后面的方法
This seems to allow the browser to store a DOM model of the page elements, so that Javascript can perform operations on it.
此处就允许浏览器保存doom原型，这样js就可以调用这个方法了
').addClass('pre-numbering').hide(); $(this).addClass('has-numbering').parent().append($numbering); for (i = 1; i <= lines; i++) { $numbering.append($('
').text(i)); }; $numbering.fadeIn(1700); }); });

无法打开网易云音乐，QQ音乐的播放页面，终端错误为在一http音频链接后This request has been blocked; the content must be served over HTTPS.[结果](http://www.voidcn.com/article/p-kmoncjvf-pm.html "结果")：
> 情况一：
无法加载JS内容写的页面。
设置setDomStorageEnabled，可能是webview前端写的一些代码便签不支持。
WebSettings settings = webview.getSettings();
settings.setJavaScriptEnabled(true);
settings.setDomStorageEnabled(true);
情况二：
出现部分内容显示部分内容不显示，打印日志大概如下：
chromium: [INFO:CONSOLE(15)] "Mixed Content: The page at 'https://dihao.moxz.cn/' was loaded over HTTPS, but requested an insecure image 'http://sm.domobcdn.com/hm/2017/landing/img/dihao/p5.jpg'. This request has been blocked; the content must be served over HTTPS.", source: https://sm.domobcdn.com/hm/2017/landing/js/swiper.3.4.2.min.js (15)
这个是加载的地址是https的，一些资源文件使用的是http方法的，从安卓4.4之后对webview安全机制有了加强，webview里面加载https url的时候，如果里面需要加载http的资源或者重定向的时候，webview会block页面加载。需要设置MixedContentMode，解决此问题的代码如下：
  WebSettings settings = webView.getSettings();
                            settings.setJavaScriptEnabled(true);
                            settings.setDomStorageEnabled(true);
                            settings.setAllowFileAccess(true);
                            settings.setAppCacheEnabled(true);
                            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                                webView.getSettings().setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
                            }

