#coding=utf-8
import urllib
import urllib2
import re

page = 1
url = 'http://www.qiushibaike.com/hot/page/'+str(page)
user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
headers = {'User-Agent':user_agent}
try:
    request  = urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile('<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?'+
                        '<div.*?Icon">(.*?)</div>.*?'+
                        '<div class="content">.*?<span>(.*?)</span>.*?'+
                        '<div class="stats">.*?<i.*?number">(.*?)</i>.*?<i.*?number">(.*?)</i>',re.S)
    items = re.findall(pattern,content)
    for item in items:
        havaImg = re.search("img",item[3])
        if not havaImg:
            print item[0],item[1],item[2],item[4]
except urllib2.URLError,e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason