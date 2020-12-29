# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import random
import os
import time

# import urllib.request

group_list = {}  # 页面内{'长发优雅气质性感美女杨晨晨sugar牛仔长裤内衣诱惑迷人私房写真': 'https://www.7160.com/meinv/68984/',
group = []  # 分页 ['https://www.7160.com/xingganmeinv/list_3_1.html', 'https://www.7160.com/xingganmeinv/list_3_2.html',

# 收集到的常用Header
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]


def send_quest(url):
    # time.sleep(0.5)
    return requests.get(url, random.choice(my_headers))


def get_group(x):
    for i in range(1, x + 1):
        group.append('https://www.7160.com/xingganmeinv/list_3_' + str(i) + '.html')


def get_group_list(group):
    for i in group:
        # print(i)
        url = 'https://www.7160.com'
        response = send_quest(i)
        response.encoding = 'gb2312'
        soup = BeautifulSoup(response.text, features='html.parser')
        div_content = soup.find(name='div', class_='news_bom-left')
        list_li = div_content.findAll(name='li')
        for i in list_li:
            a = i.find('a')
            # print(a.attrs)
            group_list[a.attrs.get('title')] = url + a.attrs.get('href')
        for i in list_li:
            a = i.find('a')
            # print(a.attrs)
            group_list[a.attrs.get('title')] = url + a.attrs.get('href')


def get_img_url(url):
    response = send_quest(url)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, features='html.parser')
    img = soup.find('img')
    # print(img.attrs.get('src'))
    return img.attrs.get('src')


def request_download(IMAGE_URL, path):
    r = send_quest(IMAGE_URL)
    with open(path, 'wb') as f:
        f.write(r.content)


def mkdir(group_list):
    # os.mkdir('图片')
    for i in group_list:
        # print(i)
        path = i.rstrip("\\")
        isExists = os.path.exists('图片/' + path)
        if not isExists:
            os.makedirs('图片/' + path)
            # print(path + ' 创建成功')
        else:
            print(' 目录已存在')


def get_img_list(url):
    response = send_quest(url)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, features='html.parser')
    div = soup.find('div', class_='itempage')
    a = div.findAll('a')
    return len(a) - 3


def read_img_list(url):
    img_url_list = []
    n = get_img_list(url)
    img_url_list.append(url + 'index.html')
    for i in range(2, n + 1):
        img_url_list.append(url + 'index_' + str(i) + '.html')
        # request_download(get_img_url(url + 'index_'+str(i)+'.html'))
    # get_img_url()
    # print(img_url_list)
    return img_url_list


if __name__ == '__main__':
    # read_img_list('https://www.7160.com/zhenrenxiu/68986/')
    n = input("===============>您需要爬取多少页的最新内容")
    n = int(n)
    get_group(n)
    get_group_list(group)
    mkdir(group_list)
    for i in group_list:
        f=0
        # print(group_list[i])
        img_url_list = read_img_list(group_list[i])
        for j in img_url_list:
            # print(j,'图片/'+i+'.jpg')
            # print(get_img_url(j))
            f+=1
            print('图片/'+i+'/'+j+'.jpg')
            request_download(get_img_url(j),'图片/'+i+'/'+str(f)+'.jpg')
