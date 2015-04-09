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
from  get_title import get_title,Title
import traceback
import datetime
import Levenshtein
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
def is_number(uchar):
	if uchar >= u'\u0030' and uchar<=u'\u0039':
		return True
	else:
		return False
def Similarity(s1,s2):

    return Levenshtein.ratio(s1,s2)
    flist  =s1.split("/")
    print "sss",flist[0].strip(),s2,Levenshtein.ratio(flist[0].strip(),s2)
    return Levenshtein.ratio(flist[0].strip(),s2)
    rate = 0.0
    for s in flist:
        r= Levenshtein.ratio(s,s2)
        if r> rate:
            rate = r
    return rate
def is_num(year):
    for c in year:
        if not is_number(c):
            return False
    return True
def get_douban_movie(parse,title):
    #print ename
    #ename ,year = get_title_year(ename)
    #print ename 
    #ename = "Le domaine des dieux"
    url="http://movie.douban.com/subject_search?search_text="
    try:
        links=[]
        need_search_by_cname = True
        if len(title.ename) > 1:
            need_search_by_cname =False
            time.sleep(1)
            lurl="http://movie.douban.com/subject_search?search_text="+title.ename
            page=urllib.urlopen(lurl).read()
     #       print "xxx",lurl
            list = parser.get_parse_data(url,page) 
            if len(list['list']) ==1:
                ltitle  = list['list'][0]['title'].encode("utf-8")
                flist  =ltitle.split("/")
                ltitle = flist[0].strip()
                return douban.get_result(list['list'][0]['link']),ltitle
            elif len(list['list']) >1 and len(list['list']) <= 12:
                links.extend(list['list'])
            else:
                need_search_by_cname =True

        if need_search_by_cname:       
            print "search by cname"
            lurl="http://movie.douban.com/subject_search?search_text="+title.cname
            url="http://movie.douban.com/subject_search?search_text="

            page=urllib.urlopen(lurl).read()

            #    print "xxx",lurl
            list = parser.get_parse_data(url,page) 
            links.extend(list['list'])
        houxuan= []
        for l in links:
            flist = l['info'].strip().split('/')
            date = flist[0][0:4]
            #print "info",l['title'],"//",l['span']
            ltitle  = l['title'].encode("utf-8")
            flist  =ltitle.split("/")
            ltitle = flist[0].strip()
#            if l['span']!=None:
#               ltitle += l['span'].encode("utf-8")
#               ltitle.replace('\n','')
            if is_num( date):
                if abs(int(date) - int(title.year)) <1:
                    houxuan.append([l,ltitle])

        houxuan.sort(key=lambda x:Similarity(x[1],title.cname),reverse=True)
        url = houxuan[0][0]['link']
        #print "DEBUG",houxuan[0][0]['info']
        item=douban.get_result(url) 
        return item ,houxuan[0][1]
    except Exception,e:

        traceback.print_exc()  
        print "ERROR:get douban movie error",e
        print "ERROR:ename =",title.ename
        print "ERROR:list = ",list
    return None,None
#print get_douban_movie("Interstellar")
def banyungong_get_link(parser):
    testurl  = "http://banyungong.net/category/101.html"
    page=urllib.urlopen(testurl).read()
    ss =  parser.get_parse_data(testurl,page)
    mlist = []
    for data in ss['list']:
        link =  "http://banyungong.net"+data['link']
        title =  data['title'].encode("utf-8")
        if "1080P电影" != title:
     #       print link,title
            t  = get_title(link,title)
            if t !=None:
                mlist.append(t)
        
    return mlist 
def gaoqingla_get_link(parser):
    mlist = []
    testurl  = "http://gaoqing.la/"
    page=urllib.urlopen(testurl).read()
    ss =  parser.get_parse_data(testurl,page)
    for data in ss['list'][0:15]:
        link =  data['link']
        title =  data['title'].encode("utf-8")
        t = get_title(link,title)
        if t !=None:
            mlist.append(t)

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
        #    print m[2],m[3],m[0],m[1]
        #sys.exit()
        #t = Title()
        #t.cname = "奇迹"
        #t.url = "http://banyungong.net/magnetm/97605d06b65049f2833feda73afbd3ac.html"
        #t.ename = "mucize"
        #t.raw = "奇迹  mucize.2015.1080p.web.dl.h.264.dd5.1.ltrg.turkish.mkv"
        #t.year = "2015"
        #mlist.append(t)
        for m in mlist:
            print "INFO:",m.cname,"////",m.ename,"/////",m.year
            it,dtitle = get_douban_movie(parse,m)
            if it != None: 
                print "INFO:",m.raw
                print "INFO:",dtitle
                if it.id not in mmap:
                    mmap[it.id] = it
    
                item = mmap[it.id]
                item.download_link.append([m.url,m.raw])
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
