"""
爬取mangabz漫画对应所有章节url
"""
import re
import time
import execjs
import requests
import urllib.parse
from bs4 import BeautifulSoup
import random
import chapter

class ChapterList:
    def __init__(self, url,path):
        self.url = url;
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Referer": self.url,
            "Cookie": "image_time_cookie=17115|637270678077155170|2"
        }
        self.path=path

    """
    获取漫画所有的章节
    """

    def get_all_chapter(self):
        try:
            res = requests.get(url=self.url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml').findAll(class_='detail-list-form-item')
            urlist = [];
            for i in soup:
                urlist.append("http://mangabz.com" + i['href'])
            comic_name=BeautifulSoup(res.text, 'lxml').find(class_="detail-info-title").text
            self.path=self.path+"\\"+str(comic_name).strip()
            return urlist, comic_name
        except:
            print("获取章节连接失败")


    def run(self):
        (urlist,comic_name)=self.get_all_chapter()
        urlist=list(reversed(urlist))
        print("正在下载---" + str(comic_name).strip() + "---" + "共" + str(len(urlist)) + "章")
        # print("输入开始的章节")
        # front=int(input())-1
        # print("输入结束的章节")
        # last=int(input())
        # #循环获取每章
        # for i in urlist[front:last]:
        #     chapter.Chapter(i,self.path).run()

        # 循环获取每章
        for i in urlist:
            chapter.Chapter(i, self.path).run()


if __name__ == '__main__':
    ##动漫url列表
    comic_urlist=[
        'http://mangabz.com/15830bz/',
        'http://mangabz.com/26047bz/',
        'http://mangabz.com/10677bz/'
    ]
    ##保存地址
    path=''

    for comic_url in comic_urlist:
        chapterList = ChapterList(url=comic_url,path=path)
        try:
            chapterList.run()
        except:
            print("下载失败")


