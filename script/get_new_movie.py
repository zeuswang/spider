# coding=utf8
import time
import urllib 
import StringIO
from pyquery import PyQuery as pyq  
from lxml import etree
import sys
import io
import os
import parse
import douban
from  get_title import get_title_year
def get_douban_movie(parse,ename):
    #print ename
    #ename ,year = get_title_year(ename)
    print ename 
    ename = "Le domaine des dieux"
    lurl="http://movie.douban.com/subject_search?search_text="+ename
    url="http://movie.douban.com/subject_search?search_text="
    page=urllib.urlopen(lurl).read()
    list = parser.get_parse_data(url,page,debug=True) 
    try:
        link = list[0]['list'][0]['link']
        print "xxxxxxxxxxxx",link
        res_list=douban.get_result(link)

        print res_list
        return res_list
    except Exception(),e:
        print e
    return None
#print get_douban_movie("Interstellar")
if __name__ == "__main__":
    parser = parse.Parser()
    parser.init(sys.argv[1])
    testurl  = "http://banyungong.net/category/101.html"
    page=urllib.urlopen(testurl).read()
    ss =  parser.get_parse_data(testurl,page,debug=True)
    for data in ss[0]['list']:
        link =  data['link']
        title =  data['title'].encode("utf-8")
        get_douban_movie(parse,title)
        break;

