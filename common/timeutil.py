import math

def get_use_time(second):
    hour = second//3600
    min = second//60 % 60
    sec = second % 3600

    return str(hour) + "小时" + str(min) + "分钟" + str(sec) + "秒"
    # return sec.__str__()