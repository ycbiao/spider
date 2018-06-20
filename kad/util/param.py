total = 100
step = 60
start = 1

baseUrl = "http://www.360kad.com"


def get_url(index):
    return baseUrl + \
        '/Category_45/' + \
        "Index.aspx/"+\
        "?page=" + str(index)


def get_detail_url(detail_url):
    return baseUrl + detail_url


def get_detail_price_url(price_url):
    return baseUrl + price_url