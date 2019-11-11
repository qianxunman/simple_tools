__author__ = 'Administrator'

import pandas as pd

data_excel = pd.read_excel('../data/test.xlsx',sheet_name=0,encoding = 'gbk')

print(data_excel,data_excel.datetime,type(data_excel))
print(dir(data_excel))
for i in data_excel:
    print(i)

data_excel.to_excel('../data/test2.xlsx',encoding='gbk')