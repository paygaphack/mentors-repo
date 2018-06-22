# import os
import csv
import pprint
import pandas as pd

DATAFILE = "UK_Gender_Pay_Gap_Data_2017_to_2018.csv"


def parse_file(datafile):
    data = []
    count = 0
    with open(datafile, "r") as f:
        r = csv.DictReader(f)
        for line in r:
            if count == 2:
                break
            data.append(line)
            count += 1
    pprint.pprint(data)
        # header_info = f.readline().split(',')
        # # print(header_info)
        # count = 0
        # for line in f:
        #     if count == 2:
        #         break
        #     comp_info = line.split(',')
        #     print('comp: ', comp_info)
        #     company_gpg_data = {}
        #     for i, header in enumerate(header_info):
        #         print(i, header, comp_info)
        #     #     company_gpg_data[header.strip()] = company_gpg_data[i].strip()
        #     # data.append(company_gpg_data)
        #     count += 1
    #
    # return data

def main():
    parse_file(DATAFILE)

if __name__ == '__main__':
    main()
