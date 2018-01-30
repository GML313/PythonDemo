#-*- coding:utf-8 -*-
import urllib,urllib2
import re
from bs4 import BeautifulSoup as bs
import requests
import Queue
import threading
import sys

headers = {'User_Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           'referer':'https://image.baidu.com'
           }
class baidusipder(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue

    # 继承自threading.Thread，并重写该方法
    def run(self):
        while not self._queue.empty():
            url = self._queue.get()
            try:
                self.get_url(url)
            except Exception,e:
                print e
                pass

    def get_url(self,url):
        r = requests.get(url=url,headers=headers)
        print r.content
        soup = bs(r.content,"html.parser")
        #注意使用find_all()方法返回的类型为<class 'bs4.element.ResultSet'>，而使用find返回的是<class 'bs4.element.Tag'>；前者是类似于list的数据结构，
        #索引只能是整数，而后者可以直接使用标签的字符串获得指定内容
        url = soup.find_all(name='div',attrs={'class':'s_tab'})[0].find(name='a',attrs={'href':re.compile(r"http://image.baidu.com/*")})
        url_img = url['href']
        print url_img
        r2 = requests.get(url=url_img,headers=headers)
        soup2 = bs(r2.content,"html.parser")
        url_img_total = soup2.find_all(name='div',attrs={'class':'imgpage'}) #.find_all(name='li',attrs={'class':'imgitem'})
        print url_img_total
        with open('./text.txt','w') as f:
            f.write(url['href']+'\n')
            f.close() #为了方便多线程读写

def main():
    f =open('./text.txt','w')
    f.close()
    queue = Queue.Queue()
    queue.put('http://www.baidu.com/s?wd=python')
    threads = []
    thread_count = 1
    for i in range(0,thread_count):
        spider = baidusipder(queue)
        threads.append(spider)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    print "It's complete!"
if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print 'no keyword! Please enter keyword:'
    #     sys.exit(-1)
    # else:
    #     main(sys.argv[1])
    main()