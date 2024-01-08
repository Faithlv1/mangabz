"""
爬取mangabz漫画对应所有章节url
"""
import requests
from bs4 import BeautifulSoup

import chapter
from util import proxyUtil


class ChapterList:
    def __init__(self, url,path):
        self.url = url;
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": self.url,
            "Cookie": "NGSERVERID=2faf5748ecd5cda6b63627cc33f222a5; frombot=1; _ga=GA1.1.1024593037.1704677605; mangabz_newsearch=%5b%7b%22Title%22%3a%22%e6%89%93%e5%b7%a5%e5%90%a7%e9%ad%94%e7%8e%8b%e5%a4%a7%e4%ba%ba%22%2c%22Url%22%3a%22%5c%2fsearch%3ftitle%3d%25E6%2589%2593%25E5%25B7%25A5%25E5%2590%25A7%25E9%25AD%2594%25E7%258E%258B%25E5%25A4%25A7%25E4%25BA%25BA%22%7d%5d; ComicHistoryitem_zh=; MANGABZ_MACHINEKEY=15b4cd67-8111-4755-b55d-b787fa0f1831; _ga_1SQXP46N58=GS1.1.1704677605.1.1.1704677617.0.0.0"
        }
        self.path=path

    """
    获取漫画所有的章节
    """

    def get_all_chapter(self):
        try:
            res = requests.get(url=self.url, headers=self.headers, timeout=10, proxies=proxyUtil.get_proxy())
            soup = BeautifulSoup(res.text, 'html.parser').findAll(class_='detail-list-form-item')
            urlist = [];
            for i in soup:
                urlist.append("http://mangabz.com" + i['href'])
            comic_name=BeautifulSoup(res.text, 'html.parser').find(class_="detail-info-title").text
            self.path=self.path+"\\"+str(comic_name).strip()
            return urlist, comic_name
        except Exception as e:
            print(e)
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
        'https://www.mangabz.com/33bz/'
    ]

    ##保存地址
    path=''

    for comic_url in comic_urlist:
        chapterList = ChapterList(url=comic_url,path=path)
        try:
            chapterList.run()
        except Exception as e:
            print(e)
            print("下载失败")


