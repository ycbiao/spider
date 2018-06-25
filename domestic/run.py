from selenium import webdriver
from bs4 import BeautifulSoup
from domestic import param
import os
from common import fileutil
import threading
import time
from common import timeutil
from common import getproxyip


# 获取详情数据
# 批准文号，
# 产品名称，
# 英文名称，
# 商品名，
#  剂型，
# 规格，
# 生产单位，
# 生产地址，
# 产品类别，
# 批准日期，
# 原批准文号，
# 药品本位码
def get_list_detail(browser,url):
    browser.get(url)

    soup = BeautifulSoup(browser.page_source, "lxml")
    tr_list = soup.find('div', attrs={'class': 'listmain'}).find_all("tr")
    data = []
    for tr in tr_list[1:13]:
        td_list = tr.find_all("td")
        string = td_list[1].getText() + "\t"
        data.append(string)
    print(data)
    return data


#  获取从arr[0]到arr[1]页列表链接内容
def get_list(arr):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        proxy_ip = getproxyip.get_fast_proxy_id()
        if proxy_ip is not "":
            chrome_options.add_argument('--proxy-server=http://101.236.35.98:8866')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        start_time = time.time()
        for index in range(arr[0],arr[1]):
            url = param.get_all_pager_url(index)
            browser.get(url)
            soup = BeautifulSoup(browser.page_source, "lxml")
            tr_list = soup.find_all("tr")
            list_data = []
            for tr in tr_list:
                a = tr.find("a")
                if a is not None:
                    url_detail = param.baseUrl + a["href"].split(",")[1].strip("'")
                    list_data.append(get_list_detail(browser,url_detail))
                    # print(url_detail)
            fileutil.create_csv(param.filename, list_data)
        browser.quit()
        use_time = int(time.time()) - int(start_time)
        print(timeutil.get_use_time(use_time))
    except Exception as e:
        print(e)


class MThread(threading.Thread):
    def __init__(self, arr):
        threading.Thread.__init__(self)
        self.arr = arr

    def run(self):
        print('starting ' + self.name)
        get_list(self.arr)


# 获取全部数据
def get_all():
    start_page = param.first_pager
    while start_page <= param.total_pager:
        MThread([start_page,start_page + param.step]).start()
        start_page += param.step


if __name__ == '__main__':

    # getproxyip.start()

    if os.path.exists(param.filename):
        os.remove(param.filename)

    list = [["批准文号","产品名称","英文名称","商品名","剂型","规格","生产单位","生产地址","产品类别","批准日期","原批准文号","药品本位码"]]
    fileutil.create_csv(param.filename,list)
    get_all()
    # get_list(browser,"http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=124356560303886909015737447882")

