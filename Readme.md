1、requests模块查看网页的html，找到指定的内容：

http://www.baidu.com/s?wd=python将关键字给wd对应的值；
从获得的页面中
```
-><div id="wrapper" class="wrapper_s"> 
->	<div class='s_tab' id="s_tab">
```
找到href="http://image.baidu.com/"开头的URL；
从新的URL页面中获得
```
-><div id="wrapper">
->	<div id="imgContainer">
->		<div id="imgid">
->			<div class="imgpage">
->				ul 
->					<li class='imgitem'>
```

2、动态页面加载与解析（JS异步加载问题）

使用Selenium调用浏览器动态加载（同时可以模拟真实使用情况，如鼠标滑动等），Beautifulsoup在解析页面时候准确性高且简便。
PhantomJS：无图形界面浏览器(selenium最新版本已经不支持了，建议使用有界面的Firefox、Chrome等)；
Selenium：自动化web测试解决方案；在selenium下使用JS模拟人为真实操作，如鼠标滚到页面末尾可以加载下面的页面；
在Chrome和IE下调用需要安装chromedirver或iedirver，内置Firefox的驱动geckodriverckod。

为了在selenium中调用Firefox，下载geckodriverckod，解压缩之后移动到/usr/local/bin目录下即可；
PhantomJS安装：解压PhantomJS到你的目录下，再将该目录加入到环境变量下，或者在调用代码时设置执行路径；
```
vim .bash_profile
export PATH="/usr/local/Cellar/phantomjs/bin:$PATH"
source .bash_profile
```
webbrowser模块-应该不具备获取动态页面的能力；

3、代理IP获取以及使用requests模块设置proxy

Chrome控制台console基本操作：
console.log: 普通信息，console.info: 提示信息，console.error:错误信息，console.warn:警告信息；
$_返回最近一次表达式执行结果，$0-$4表示最近5个你选择过的DOM节点，$(selector)返回满足选择条件的首个DOM元素；