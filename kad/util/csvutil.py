import csv

filename = 'kad_csv.csv'


def create_csv(file_name,kad_list):
    with open(file_name,'a', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for cell in kad_list:
            csv_writer.writerow(cell)

if __name__ == '__main__':

    kads = [["1","2","3"],["1","2","3"]]

    create_csv(filename,kads)