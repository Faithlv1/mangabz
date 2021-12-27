"""
爬取mangabz单个章节漫画
"""
import os
import re
import time
import execjs
import requests
import urllib.parse
from bs4 import BeautifulSoup
import random


class Chapter:
    """
    url:对应章节url
    path对应保存的路径
    """

    def __init__(self, url, comic_name):
        self.url = url
        self.path=comic_name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Referer": 'http://mangabz.com/5519bz/',
            "Cookie": "image_time_cookie=17115|637270678077155170|2",
        }

    """
    获取构建图片文件url的值
    """

    def get_js(self):
        try:
            res = requests.get(url=self.url, headers=self.headers, timeout=10)
            soup=BeautifulSoup(res.text,'lxml')
        except:
            print("章节rquest错误")

        mangabz_cid = re.findall("MANGABZ_CID=(.*?);", res.text)[0]
        mangabz_mid = re.findall("MANGABZ_MID=(.*?);", res.text)[0]
        page_total = re.findall("MANGABZ_IMAGE_COUNT=(.*?);", res.text)[0]
        mangabz_viewsign_dt = re.findall("MANGABZ_VIEWSIGN_DT=\"(.*?)\";", res.text)[0]
        mangabz_viewsign = re.findall("MANGABZ_VIEWSIGN=\"(.*?)\";", res.text)[0]

        soup=BeautifulSoup(res.text,'lxml').find(class_="top-title")

        chapter_name=str(soup.text).strip()
        return (mangabz_cid, mangabz_mid, mangabz_viewsign_dt, mangabz_viewsign, page_total,chapter_name)

    def get_js_url(self, mangabz_cid, page, mangabz_mid, mangabz_viewsign_dt, mangabz_viewsign):
        js_url = self.url + (
                    "chapterimage.ashx?" + "cid=%s&" + "page=%s&" + "key=&" + "_cid=%s&" + "_mid=%s&" + "_dt=%s&" + "_sign=%s") % (
                     mangabz_cid, page, mangabz_cid, mangabz_mid, urllib.parse.quote(mangabz_viewsign_dt),
                     mangabz_viewsign)
        return js_url


    def get_image_url(self, js_url):
        try:
            res = requests.get(url=js_url, headers=self.headers, timeout=10)
            self.headers['Referer'] = res.url
            js_str = res.text
            imagelist = execjs.eval(js_str)
            return imagelist[0]
        except TimeoutError:
            print("获取图片连接失败")

    def down_image(self, image_url, page):
        try:
            if not os.path.isdir(self.path):
                os.makedirs(self.path)
        except:
            print("文件夹创建失败")

        ##判断图片是否已经存在
        try:
            if os.path.isfile(self.path+'/'+str(page).strip() + ".png"):
                return 0
        except:
            print("判断图片存在失败")

        try:
            res = requests.get(url=image_url, headers=self.headers, timeout=10)
            content = res.content
            with open(self.path+'/'+str(page) + ".png", 'wb') as f:
                f.write(content)
            print("成功下载" + str(page) + "页")
        except:
            print("下载错误"+str(page)+"页")
            print(image_url)

        # time.sleep(0.2)

    def run(self):
        (mangabz_cid, mangabz_mid, mangabz_viewsign_dt, mangabz_viewsign, page_total,chapter_name) = self.get_js()
        self.path=self.path+"/"+str(chapter_name)
        #若已经有该章节的文件夹，判断是否下载完全，下载过就不下了
        if os.path.exists(self.path):
            files=os.listdir(self.path)
            num_png=len(files)
            #如果文件数等于页数，表示下载完了
            if num_png==int(page_total):
                print(str(chapter_name)+" 已经下载")
                return
        print("正在下载" + str(chapter_name) + "---" + "共" + str(page_total) + "页")
        for i in range(int(page_total)):
            js_url = self.get_js_url(mangabz_cid, i+1, mangabz_mid, mangabz_viewsign_dt, mangabz_viewsign)
            image_url = self.get_image_url(js_url)
            self.down_image(image_url, i+1)


# if __name__ == '__main__':
#
#
#     chapter = Chapter("http://mangabz.com/m204833/","")
#     chapter.run()
