import requests
from bs4 import BeautifulSoup

url = 'https://www.yiibai.com/manual/postgresql/index.html'


res = requests.get(url).content.decode('utf-8')

# 获取主页中的网址信息,以及标题信息:

# 正则表达式:
reg = r''
bs_res = BeautifulSoup(res)

for i in bs_res.select('a'):
    print (i,type(i),i.get('href','找不到'),i.text)
# print(bs_res)

print(type(bs_res))