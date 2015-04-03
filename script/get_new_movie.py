# coding=utf8
import time
import urllib 
import urllib2
import StringIO
from pyquery import PyQuery as pyq  
from lxml import etree
import sys
import io
import os
import parse
import douban
from  get_title import get_title
import traceback
import datetime
def download_pic(url,id,dir):
    try:
        if not os.path.exists(dir):  
            os.mkdir(dir)  
        path = dir+"/"+id+".jpg" 
        data = urllib.urlopen(url).read()  
        f = file(path,"wb")  
        f.write(data)  
        f.close()  
    except Exception,e:
        traceback.print_exc()  
        print e

def get_douban_movie(parse,ename):
    #print ename
    #ename ,year = get_title_year(ename)
    #print ename 
    #ename = "Le domaine des dieux"
    lurl="http://movie.douban.com/subject_search?search_text="+ename
    url="http://movie.douban.com/subject_search?search_text="
    page=urllib.urlopen(lurl).read()
    list = parser.get_parse_data(url,page) 
    try:
        link = list[0]['list'][0]['link']
        item=douban.get_result(link)

        return item
    except Exception,e:

        traceback.print_exc()  
        print "ERROR:get douban movie error",e
        print "ERROR:ename =",ename
        print "ERROR:list = ",list
    return None
#print get_douban_movie("Interstellar")
def banyungong_get_link(parser):
    testurl  = "http://banyungong.net/category/101.html"
    page=urllib.urlopen(testurl).read()
    ss =  parser.get_parse_data(testurl,page)
    mlist = []
    for data in ss[0]['list']:
        link =  "http://banyungong.net"+data['link']
        title =  data['title'].encode("utf-8")
        if "1080P电影" != title:
            title2 = get_title(link,title)
            if title2 !=None:
                mlist.append([link,title,title2])
    return mlist 
def gaoqingla_get_link(parser):
    mlist = []
    testurl  = "http://gaoqing.la/"
    page=urllib.urlopen(testurl).read()
    ss =  parser.get_parse_data(testurl,page)
    for data in ss[0]['list']:
        link =  data['link']
        title =  data['title'].encode("utf-8")
        title2 = get_title(link,title)
        if title2 !=None:
            mlist.append([link,title,title2])
    return mlist
if __name__ == "__main__":
    try:
        mmap = {}
        output_movie = sys.argv[2]
        output_link = sys.argv[3]
        pic_dir = sys.argv[4]
        parser = parse.Parser()
        parser.init(sys.argv[1])
        mlist = []
        mlist.extend(banyungong_get_link(parser))
        mlist.extend(gaoqingla_get_link(parser))
        #for m in mlist:
        #    print m[2],m[0],m[1]
        #sys.exit()
        for m in mlist:
            print "INFO:",m[2],m[0],m[1]
            it = get_douban_movie(parse,m[2])
            if it != None: 
                print "INFO:","get ok",m[2]
                if it.id not in mmap:
                    mmap[it.id] = it
    
                item = mmap[it.id]
                item.download_link.append([m[0],m[1]])
                time.sleep(1)
                download_pic(item.pic_url,item.id,pic_dir)
                time.sleep(1)
            time.sleep(1)
    #    print mmap
        fp = open(output_movie,'w')
        for k,it in mmap.items():
            str = '%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\3%s\n' % (it.id,it.cname,it.ename,it.actors,it.director,it.writer,it.location,it.type,it.date,it.runtime,it.rate,it.votes,it.pic_url,it.aname,it.imdb_link,it.comment_link,it.summary)
            fp.write(str)
        fp.close()
        time = datetime.datetime.now()
        datestr = time.strftime('%Y-%m-%d')
        fp = open(output_link,'w')
        for k,v in mmap.items():
    #        print k
            
            for dl in v.download_link:
                str = '%s\3%s\3%s\3%s\n' % (k,dl[0],dl[1],datestr)
                fp.write(str)
        fp.close()
    except Exception,e:
        print traceback.print_exc()
        print e
