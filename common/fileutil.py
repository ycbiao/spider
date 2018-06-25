import csv


# 创建csv文件
def create_csv(file_name,list):
    with open(file_name,'a', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for cell in list:
            csv_writer.writerow(cell)


#
if __name__ == '__main__':
    kads = [["1","2","3"],["1","2","3"]]
    filename = 'kad_csv.csv'
    create_csv(filename,kads)