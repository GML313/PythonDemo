#-*- coding: utf-8 -*-
import urllib,urllib2
import re
from bs4 import BeautifulSoup
import pymysql.cursors
import requests
import json

"""
url = 'https://en.wikipedia.org/wiki/Main_Page'
request = urllib2.Request(url)
resp = urllib2.urlopen(request)
#print resp.info()
soup = BeautifulSoup(resp,"html.parser")#使用解析器解析HTML(BS默认有三种解析器)，不同的解析器会获得不同结构的树形文档
#默认输出编码方式为UTF-8
listUrls = soup.findAll("a",href=re.compile("^/wiki/"))
for url in listUrls:
    if not re.search(r"\.(jpg|JPG|png)$",url["href"]):
        print url.get_text(), "<---->", "https://en.wikipedia.org"+url["href"]
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='Gml_2018',
                                     db='wikiurl',
                                     charset='utf8mb4')
        try:
            with connection.cursor() as cursor:
                #sql = "insert into `urls`(`urlname`,`urlhref`)values(%s,%s)"
                #cursor.execute(sql, (url.get_text(), "https://en.wikipedia.org" + url["href"]))
                sql = "select * from urls"
                cursor.execute(sql)
                #connection.commit()
        finally:
            connection.close()
"""
def download_image():
    url = 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=3849388262,3599136548&fm=27&gp=0.jpg'
    headers = {'User_Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get(url,headers=headers,stream=True)
    from contextlib import closing
    with closing(requests.get(url,headers=headers,stream=True)) as response:
        with open('demo.jpg','wb') as fb:
            for chunk in response.iter_content(128):
                fb.write(chunk)
def get_key_info(response,*args,**kwargs):
    print response.headers['Content-type']
def hook_test():#事件回调机制
    requests.get('http://www.baidu.com/',hooks=dict(response=get_key_info))

class GithubApi(object):
    URL = 'https://api.github.com'
    def use_simple_requests(self):
        url = 'http://httpbin.org/ip'
        params = {'parm1':'hello','param2':'world'}
        response = requests.get(url,params=params)
        #response = urllib2.urlopen(url+'?'+request)
        print '>>>>response headers:'
        print response.headers
        print '>>>>reponse status code:'
        print response.status_code
        print '>>>reponse body:'
        print response.json()
    def json_request(self):
        data = GithubApi.URL+'/'+'user/emails'
        response = requests.get(data,auth=('imoocdemo','imoocdemo123'))
        print response.text
    def timeout_request(self):
        try:
            data = GithubApi.URL+'/'+'user/emails'
            response = requests.get(data,timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            print e.message
        except requests.exceptions.HTTPError as e:
            print e.message
        else:
            print response.text
            print response.status_code
    def hard_requests(self):
        from requests import Request,session
        data = GithubApi.URL+'/'+'user/emails'
        s = session()
        headers = {'User-Agent':'fake1.3.4'}
        req = Request('GET',data,auth=('imoocdemo','imoocdemo123'),headers=headers)
        prepped = req.prepare()
        print prepped.body
        print prepped.headers
        resp = s.send(prepped,timeout=5)
        print resp.headers
        print resp.status_code
        print resp.history
        print resp.elapsed
if __name__ == '__main__':
    insta1 = GithubApi()
    #insta1.use_simple_requests()
    #insta1.timeout_request()
    #insta1.hard_requests()
    #download_image()
    hook_test()
    data={'a':1,'b':2}
    text = json.dumps(data)
    print text
    print json.loads(text)

"""
user
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
headers = {'User_Agent':user_agent}
values = {'wd':'D_in'}
data = urllib.urlencode(values)
request = urllib2.Request(url,data,headers)
response = urllib2.urlopen(request)
page = response.read()
url2 = url + '?' + data
#for k, v in response.getheaders():
   print('%s: %s' % (k, v))
print('Data:', data.decode('utf-8'))
"""
# str = '16_7@163.com'
# pa = re.compile(r'^\w{0,19}@163.(com|cn|net|org){1,3}$')
# print re.search(pa,str).group()
