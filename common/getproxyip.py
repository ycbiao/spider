# -*- coding: utf-8 -*-
import urllib

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from selenium import webdriver
import time
import requests

# HOME_URL = 'http://www.xicidaili.com/'  # 首页代理IP
# ANONY_URL = 'http://www.xicidaili.com/nn/'  # 国内高匿代理IP
# NORMAL_URL = 'http://www.xicidaili.com/nt/'  # 国内普通代理IP
# HTTP_URL = 'http://www.xicidaili.com/wt/'  # 国内HTTP代理IP
HTTPS_URL = 'http://www.xicidaili.com/wn/'  # 国内HTTPS代理IP
HEADERS = {
    'Host': 'www.xicidaili.com',
    'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}


def get_ip(obj):
    counter = 0
    sec_obj = obj.find('table')
    ip_text = sec_obj.findAll('tr')  # 获取带有IP地址的表格的所有行
    if ip_text is not None:
        with open('Proxy-IP.txt', 'r+') as f:    # 保存到本地txt文件中
            for i in range(1, len(ip_text)):
                ip_tag = ip_text[i].findAll('td')
                ip_live = ip_tag[8].get_text()  # 代理IP存活时间
                ip_speed = ip_tag[6].find('div', {'class': 'bar_inner fast'})  # 提取出速度快的IP
                if '天' in ip_live and ip_speed:
                    ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text()  # 提取出IP地址和端口号
                    counter += 1
                    if valVer(ip_port) == 1:
                        f.write(ip_port + '\n')
                        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' -- ' + 'Got %s proxy IPs.')


# 检测代理可用性
def valVer(proxy):
    state = 0
    try:
        proxy_host = proxy
        protocol = 'https' if 'https' in proxy_host else 'http'
        proxies = {protocol: proxy_host}
        response = requests.get('http://www.baidu.com', proxies=proxies, timeout=2)
        if response.status_code != 200:
            # print(proxy_host, 'bad proxy')
            state = 0
        else:
            print(proxy_host, 'success proxy')
            state = 1
    except Exception:
        print(Exception)

    return state

def  get_proxy_id():
    proxy = ""
    file = open('Proxy-IP.txt')
    while 1:
        line = file.readline()
        for line1 in line:
            proxy = line1
    file.close()
    return proxy

def start(URL):
    while True:
        request = Request(URL, headers=HEADERS)
        response = urlopen(request)
        bsObj = BeautifulSoup(response, 'lxml')  # 解析获取到的html
        get_ip(bsObj)
        time.sleep(900)  # 每十五分钟更新一次


if __name__ == '__main__':
    start(HTTPS_URL)