"""
爬取mangabz单个章节漫画
"""
import os
import re
import time
import urllib.parse

import execjs
import requests
from bs4 import BeautifulSoup

from util import proxyUtil


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
            "Referer": 'https://www.mangabz.com/',
            "Cookie": "frombot=1; _ga=GA1.1.1024593037.1704677605; MANGABZ_MACHINEKEY=15b4cd67-8111-4755-b55d-b787fa0f1831; mangabz_newsearch=%5b%7b%22Title%22%3a%22%e6%89%93%e5%b7%a5%e5%90%a7%e9%ad%94%e7%8e%8b%e5%a4%a7%e4%ba%ba%22%2c%22Url%22%3a%22%5c%2fsearch%3ftitle%3d%25E6%2589%2593%25E5%25B7%25A5%25E5%2590%25A7%25E9%25AD%2594%25E7%258E%258B%25E5%25A4%25A7%25E4%25BA%25BA%22%7d%2c%7b%22Title%22%3a%22%e6%89%93%e5%b7%a5%e5%90%a7%22%2c%22Url%22%3a%22%5c%2fsearch%3ftitle%3d%25E6%2589%2593%25E5%25B7%25A5%25E5%2590%25A7%22%7d%5d; mangabzcookieenabletest=1; _ga_1SQXP46N58=GS1.1.1704682144.3.1.1704682186.0.0.0; mangabzimgcooke=326707%7C3%2C335903%7C2; ComicHistoryitem_zh=History=33,638403077939859328,335903,2,0,0,0,215&ViewType=0; readhistory_time=1-33-335903-2; image_time_cookie=306617|638403057908853380|0,326707|638403077605342832|1,335903|638403077940189549|1; mangabzimgpage=306617|1:1,326707|2:1,335903|2:1",
        }

    """
    获取构建图片文件url的值
    """

    def get_js(self):
        try:
            res = requests.get(url=self.url, headers=self.headers, timeout=10, proxies=proxyUtil.get_proxy())
            soup = BeautifulSoup(res.text,'html.parser')
        except Exception as e:
            print(e)
            print("章节rquest错误")

        mangabz_cid = re.findall("MANGABZ_CID=(.*?);", res.text)[0]
        mangabz_mid = re.findall("MANGABZ_MID=(.*?);", res.text)[0]
        page_total = re.findall("MANGABZ_IMAGE_COUNT=(.*?);", res.text)[0]
        mangabz_viewsign_dt = re.findall("MANGABZ_VIEWSIGN_DT=\"(.*?)\";", res.text)[0]
        mangabz_viewsign = re.findall("MANGABZ_VIEWSIGN=\"(.*?)\";", res.text)[0]

        soup = BeautifulSoup(res.text,'html.parser').find(class_="top-title")

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
            res = requests.get(url=js_url, headers=self.headers, timeout=10, proxies=proxyUtil.get_proxy())
            self.headers['Referer'] = res.url
            js_str = res.text
            imagelist = execjs.eval(js_str)
            return imagelist[0]
        except TimeoutError:
            print("获取图片连接失败")

    def down_image(self, image_url, page):
        print("正在下载" + str(page) + "页")
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
            res = requests.get(url=image_url, headers=self.headers, timeout=10, proxies=proxyUtil.get_proxy())
            content = res.content
            with open(self.path+'/'+str(page) + ".png", 'wb') as f:
                f.write(content)
            print("成功下载" + str(page) + "页")
        except:
            print("下载错误"+str(page)+"页")
            print(image_url)



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
            time.sleep(1)
