#-*-coding:utf-8-*-
'''
author:xzg
'''
import requests
import sys
import MySQLdb
import re
import csv
import pandas
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

#获取页面
def get_page(page):
    url = 'https://movie.douban.com/top250/?start=' + page + '&filter='
    response = requests.get(url).text         #获取页面源码，text表示返回Unicode数据
    return response

#解析页面，获取数据
def parse_html(html):
    movie_name_list = []        #电影名称
    star_count_list = []        #评价人数
    rating_num_list = []        #评分
    inq_list = []               #短评
    soup = BeautifulSoup(html,'lxml')
    ol = soup.find('ol','grid_view')
    for li in ol.find_all('li'):
        movie_name = li.find('span','title').string
        rating_num = li.find('span','rating_num').string
        star_count = li.find(text = re.compile(u'评价'))
        inq = li.find('span','inq')
        if inq:
            inq_list.append(inq.string)
        else:
            inq_list.append('')
        movie_name_list.append(movie_name)
        star_count_list.append(star_count)
        rating_num_list.append(rating_num)

    return movie_name_list,star_count_list,rating_num_list,inq_list

#将数据存入mysql数据库
def put_db(movie_name_list,star_count_list,rating_num_list,inq_list):
    db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='spider', charset='utf8')  # 建立数据库连接
    cur = db.cursor()  # 创建游标
    sql = 'insert into douban_top_250(movie_name,star_count,rating_num,inq) values (%s,%s,%s,%s)'
    #print len(movie_name_list),len(star_count_list),len(rating_num_list),len(inq_list)
    for i in range(0,len(movie_name_list)):
       param = (movie_name_list[i],star_count_list[i],rating_num_list[i],inq_list[i])
       cur.execute(sql,param)
    db.commit()

#通过pandas将数据保存为csv文件
def save_csv(movie_name_list,star_count_list,rating_num_list,inq_list):
    data = {'movie_name':movie_name_list,'star_count':star_count_list,'rating_num':rating_num_list,'inq':inq_list}
    dataframe = pandas.DataFrame(data)
    dataframe.to_csv(r'C:\Users\Administrator\Desktop\test.csv',index = False,sep = ',',encoding='utf_8_sig')        #加编码不然会中文乱码

#将文件发送邮箱
def test_smtp():
    pass

def main():
    movie_name_list = []  # 电影名称
    star_count_list = []  # 评价人数
    rating_num_list = []  # 评分
    inq_list = []
    for page in range(0,226,25):
        response = get_page(str(page))
        movie_name, star_count, rating_num, inq = parse_html(response)
        movie_name_list += movie_name
        star_count_list += star_count
        rating_num_list += rating_num
        inq_list += inq
    put_db(movie_name_list,star_count_list,rating_num_list,inq_list)
    save_csv(movie_name_list, star_count_list, rating_num_list, inq_list)
    print 'ending spider'
    #print ','.join(movie_name_list)
    #print ','.join(star_count_list)
    #print rating_num_list
    #print ''.join(inq_list)

if __name__ == '__main__':
    main()