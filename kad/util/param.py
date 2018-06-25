total = 1
step = 1
start = 1

baseUrl = "http://www.360kad.com"
filename = 'kad_csv.csv'

def get_url(index):
    return baseUrl + \
        '/Category_45/' + \
        "Index.aspx/"+\
        "?page=" + str(index)


def get_detail_url(detail_url):
    return baseUrl + detail_url


def get_detail_price_url(price_url):
    return baseUrl + price_url