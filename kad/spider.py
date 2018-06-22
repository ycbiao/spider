# -*- coding: utf-8 -*-
# 康爱多网页抓取数据
import os
import threading
import time

from bs4 import BeautifulSoup
from selenium import webdriver

from common import fileutil
from kad.util import param


# 获取规格和价格
def get_detail_certification_price(browser,url):

    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "lxml")
    # print(soup.prettify())
    specification = soup.find('div', attrs={'id': 'spec_box'}).find("li", attrs={'class': 'dtl-inf-rur'}).getText()
    price = soup.find('span', attrs={'id': 'saleprice_value'}).getText()
    str_price = "规格:" + specification + "/价格:" + price
    # print(str_price)
    return str_price


# 子页
def get_detail(browser,url):
    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())
        li = soup.find('div', attrs={'id': 'spec_box'}).find_all("li")
        specification_price_list = []
        for a in li:
            str = a.a["href"]
            if str.startswith("/",0,len(str)):
                # print(str)
                str_p = get_detail_certification_price(browser,param.get_detail_url(str))
                specification_price_list.append(str_p)
            else:
                price = soup.find('span', attrs={'id': 'saleprice_value'}).getText()
                specification = a.getText()
                specification_price_list.append("规格:" + specification + "/价格:" + price)

    except Exception as ex:
        print(ex)

    return specification_price_list


# 所有药品
def get_all_paper(arr):
    start_time = time.time()
    # browser = webdriver.Chrome("G:\chromedownlaods\chromedriver_win32\chromedriver.exe") 未配置chromedrive环境变量需要制定path
    chrome_options = webdriver.ChromeOptions()
    # chrome无头模式不打开页面
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # PROXY = "113.86.222.104:60443"  # IP:PORT or HOST:PORT
    # chrome_options.add_argument('--proxy-server=http://127.0.0.1:1080')
    # chrome_options.add_argument('--proxy-server=http://171.37.135.94:8123')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    for i in range(arr[0],arr[1]):
        url = param.get_url(i)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "lxml")
        li = soup.find('ul', attrs={'id': 'YproductList'}).find_all('li')
        kad_list = []
        for cell in li:
            cell_list = []
            a = cell.find('p', attrs={'class': 'Ypic'})
            detail_url = a.a["href"]
            price_list = get_detail(browser, param.get_detail_url(detail_url))

            src = cell.img["src"]
            name = cell.find('a', attrs={'class': 'name'})["title"]
            # price = re.findall('(\w*[0-9]+)\w*',cell.find('span', attrs={'class': 'RMB'}).getText())[0]
            cell_list.append(name)
            cell_list.append(src)
            # cell_list.append(price)
            for price_list_cell in price_list:
                cell_list.append(price_list_cell)
            print(str(cell_list))
            kad_list.append(cell_list)

        fileutil.create_csv(fileutil.filename, kad_list)

    browser.quit()
    use_time = int(time.time()) - int(start_time)
    print(time.strftime("%H:%M:%S", time.localtime(use_time)))


def get_all():
    if os.path.exists(fileutil.filename):
        os.remove(fileutil.filename)

    while param.start <= param.total:
        t = SpiderThread([param.start, param.start + param.step])
        t.start()
        param.start += param.step


class SpiderThread(threading.Thread):
    def __init__(self, arr):
        threading.Thread.__init__(self)
        self.arr = arr

    def run(self):
        print('starting ' + self.name)
        get_all_paper(self.arr)


if __name__ == '__main__':
    get_all()
