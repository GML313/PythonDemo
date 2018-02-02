#-*- coding:utf-8 -*-
import urllib,urllib2
import re
from bs4 import BeautifulSoup as bs
import requests
import Queue
import threading
import multiprocessing
from multiprocessing import cpu_count
import sys
from selenium import webdriver
import time
import random

# 将发送给服务器的请求使用浏览器的头加以伪装
# 'referer':'https://image.baidu.com'   'Accept-Language:':'zh-CN,zh;q=0.8',
headers = {
    'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}

# 配置selenium打开的浏览器，默认支持Firefox
# 注意：最新版的selenium不在支持phantomjs内嵌式浏览器
# firefox_profile = webdriver.FirefoxProfile()
# firefox_profile.set_preference('permissions.default.image',2)
# firefox_profile.set_preference("permissions.default.stylesheet",2)
# firefox_profile.update_preferences()
# driver = webdriver.Firefox(firefox_profile=firefox_profile)
#设置phantomjs配置优化加载速度
service_args = []
service_args.append('--load-images=no')  ## 关闭图片加载

class baiduspider(multiprocessing.Process):
    driver = webdriver.PhantomJS(executable_path=r'/usr/local/Cellar/phantomjs/bin/phantomjs',
                                 service_args=service_args)
    # driver = webdriver.Firefox(firefox_profile=firefox_profile)
    def __init__(self,queue):
        multiprocessing.Process.__init__(self)
        self._queue = queue

    # 继承自threading.Thread，并重写该方法
    def run(self):
        print 'Get Picture URL From baidu:'
        while not self._queue.empty():
            url = self._queue.get()
            try:
                self.get_url(url)
                baiduspider.driver.quit()
                print "Picture Get!"
            except Exception,e:
                print e
                baiduspider.driver.quit()
                pass

    #直接关键词百度出来内容，并获得对应图片网页，将相应的图片地址获得
    def get_url(self,url):
        r = requests.get(url=url,headers=headers)
        soup = bs(r.content,"html.parser")
        #注意使用find_all()方法返回的类型为<class 'bs4.element.ResultSet'>，而使用find返回的是<class 'bs4.element.Tag'>；前者是类似于list的数据结构，
        #索引只能是整数，而后者可以直接使用标签的字符串获得指定内容
        url = soup.find_all(name='div',attrs={'class':'s_tab'})[0].find(name='a',attrs={'href':re.compile(r"http://image.baidu.com/*")})
        url_img = url['href']
        print url_img

        baiduspider.driver.get(url_img)
        #模拟JS，将webpage滚动至页面最下面，加载更多的图片
        # driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        # time.sleep(1)
        soup = bs(baiduspider.driver.page_source,'lxml') #注意不同的解析器，可能会页面不同，这个有待进一步尝试
        driver_page = soup.find_all(name='li',attrs={'class':'imgitem'})
        url_subimg = []
        for i in range(0,len(driver_page)):
            #print driver_page[i]['data-objurl']
            url_subimg.append(driver_page[i]['data-objurl']+'\n')
        with open('./picture_url.txt', 'w') as f:
            for i in url_subimg:
                f.write(i)
            f.close()  # 为了方便多线程读写

class proxyspider(multiprocessing.Process):
    driver = webdriver.PhantomJS(executable_path=r'/usr/local/Cellar/phantomjs/bin/phantomjs',
                                 service_args=service_args)
    # driver = webdriver.Firefox(firefox_profile=firefox_profile)
    def run(self):
        print "Proxy Test:"
        try:
            self.get_proxy()
            print 'Get Proxy IP!'
            self.link_webpage()
            print 'Proxy Complete!'
            proxyspider.driver.quit()
        except Exception, e:
            print e
            proxyspider.driver.quit()  # 保证出现采集代理出现异常，依旧可以正常关闭plantomjs
            pass

    #从代理网站获取代理IP
    def get_proxy(self):

        # try:
        #     proxy_url = requests.get(url=url,headers=headers)
        #     print proxy_url.raise_for_status()
        # except requests.RequestException as e:
        #     print e
        # else:
        #     result = proxy_url.text
        #     print type(result),result

        #获取动态页面
        url = 'http://www.site-digger.com/html/articles/20110516/proxieslist.html'
        pattern = r'\d{2,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}' #如何获得更加简洁高效的正则表达式？
        proxyspider.driver.get(url)
        #print driver.page_source
        soup = bs(proxyspider.driver.page_source,'lxml')
        proxy_tr = soup.find_all(name='tr')
        #print proxy_tr
        with open('./proxy_url.txt', 'w') as f:
            for i in range(0,len(proxy_tr)):
                tmp = proxy_tr[i].find_all(name='td')
                tmp_ip = re.search(pattern,str(tmp))
                if tmp_ip : f.write(tmp_ip.group()+'\n')
            f.close()


    #使用代理IP实现代理功能
    def link_webpage(self):
        with open('proxy_url.txt', 'r') as open_proxy:
            proxy_tmp = open_proxy.readlines()
        #open_proxy.close()
        one_proxy = random.choice(proxy_tmp)
        proxies = {"http": ('http://' + one_proxy).replace("\n", ""),"https":('http://' + one_proxy).replace("\n", "")}
        print proxies
        #num = raw_input()
        #url = 'https://btdigg.org/search?info_hash=&q=' + num
        #url = 'https://zhuanlan.zhihu.com/p/25507989'
        url = 'https://www.baidu.com'
        firewall_page = requests.get(url=url,headers=headers,timeout=30) #,proxies=proxies
        print firewall_page

def main():
    # 不是批量使用，暂时不需要进程池  pool(processes=2)
    start = time.time()
    print 'The number of CPU: ',cpu_count()
    f =open('./picture_url.txt','w')
    f.close()
    queue = Queue.Queue() #缓存队列
    queue.put('http://www.baidu.com/s?wd=python')

    processes = []
    # thread_count = 2 #线程数量设置
    # for i in range(0,thread_count):
    #     spider = baidusipder(queue)
    #     threads.append(spider)

    picture = baiduspider(queue)
    proxy = proxyspider()
    processes.append(proxy)
    processes.append(picture)

    for i in processes:
        i.start()
    for i in processes:
        i.join()
    end = time.time()
    print (end-start)
if __name__ == '__main__':
    #可以出入参数作为搜索图片的关键词
    # if len(sys.argv) != 2:
    #     print 'no keyword! Please enter keyword:'
    #     sys.exit(-1)
    # else:
    #     main(sys.argv[1])
    main()