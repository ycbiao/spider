# -*- coding: utf-8 -*-
import urllib

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import os
import time
import requests
from common import timeutil
from operator import itemgetter, attrgetter

# HOME_URL = 'http://www.xicidaili.com/'  # 首页代理IP
# ANONY_URL = 'http://www.xicidaili.com/nn/'  # 国内高匿代理IP
# NORMAL_URL = 'http://www.xicidaili.com/nt/'  # 国内普通代理IP
HTTP_URL = 'http://www.xicidaili.com/wt/'  # 国内HTTP代理IP
# HTTPS_URL = 'http://www.xicidaili.com/wn/'  # 国内HTTPS代理IP
HEADERS = {
    'Host': 'www.xicidaili.com',
    'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
filename = "C:\workplace\spiderpy\Proxy-IP.txt"


def get_ip(obj,test_url):
    counter = 0
    sec_obj = obj.find('table')
    ip_text = sec_obj.findAll('tr')  # 获取带有IP地址的表格的所有行
    if ip_text is not None:
        with open(filename, 'w+') as f:    # 保存到本地txt文件中
            for i in range(1, len(ip_text)):
                ip_tag = ip_text[i].findAll('td')
                ip_live = ip_tag[8].get_text()  # 代理IP存活时间
                ip_speed = ip_tag[6].find('div', {'class': 'bar_inner fast'})  # 提取出速度快的IP
                if '天' in ip_live and ip_speed:
                    ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text()  # 提取出IP地址和端口号
                    counter += 1
                    check_state = check_proxy_availability(ip_port,test_url)
                    if check_state[0] == 1:
                        ip_port += ";"+check_state[1].__str__()
                        f.write(ip_port + '\n')
                        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' -- ' + 'Got %s proxy IPs.')
            f.close()
            print("get proxy IPs process end")


# 检测代理可用性
def check_proxy_availability(proxy,test_url):
    state = 0
    use_time = 0
    try:
        start_time = time.time()
        proxy_host = proxy
        protocol = 'https' if 'https' in proxy_host else 'http'
        proxies = {protocol: proxy_host}
        response = requests.get(test_url, proxies=proxies, timeout = 5)
        if response.status_code != 200:
            # print(proxy_host, 'bad proxy')
            state = 0
        else:
            use_time = int(time.time()) - int(start_time)
            print(proxy_host, 'success proxy，time = '+ timeutil.get_use_time(use_time).__str__())
            state = 1
    except Exception as e:
        print(e)
    finally:
        return [state, use_time]


# 从Proxy-IP.txt获取速度最快代理ip
def get_fast_proxy_id():
    proxy_fast = ""
    try:
        # 默认路径在当前运行脚本，所以其他脚本运行时调用不到该文件
        with open(filename, 'r') as file:
            file.seek(0)
            line = file.readlines()
            proxy_fast = line[0]
            for line1 in line:
                line1.strip("\n")
                proxy_fast_state = proxy_fast.split(";")[1]
                line1_state = line1.split(";")[1]
                if int(line1_state) < int(proxy_fast_state):
                    proxy_fast = line1

            file.close()
    except Exception as e:
        print(e)
    print(filename + "最快代理：" + proxy_fast)
    return proxy_fast.split(";")[0]


def start(test_url):
    if os.path.exists(filename):
        os.remove(filename)
    # while True:
    request = Request(HTTP_URL, headers=HEADERS)
    response = urlopen(request)
    bsObj = BeautifulSoup(response, 'lxml')  # 解析获取到的html
    get_ip(bsObj,test_url)
        # time.sleep(900)  # 每十五分钟更新一次


if __name__ == '__main__':

    start()
    get_fast_proxy_id()