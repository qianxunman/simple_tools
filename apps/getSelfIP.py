"""
利用百度简单获取本机的公网IP地址。
"""

import requests
import re

url = 'https://www.baidu.com/s?wd=ip&rsv_spt=1&rsv_iqid=0xb9280ba7000022f9&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=3&rsv_sug1=2&rsv_sug7=100&rsv_sug2=0&inputT=563&rsv_sug4=1617'
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate, br',
'Upgrade-Insecure-Requests': '1',
'Connection': 'keep-alive',
'Cookie': 'BAIDUID=04DFDDA791D996A095561798337DA67C:FG=1;' \
          ' BIDUPSID=04DFDDA791D996A095561798337DA67C; PSTM=1551618278;' \
          'BD_UPN=13314752; delPer=0; BD_HOME=0; H_PS_PSSID=1454_21106_18559_28584_28558_28519;' \
          ' BD_CK_SAM=1; PSINO=7; H_PS_645EC=07a5EGDIVlnpzZ0vL5' \
          'sZ7hN5c22qv53chwtk5J6a1YlsYSenHsyA4Fl%2Bz3g; BDORZ=B490B5' \
          'EBF6F3CD402E515D22BCDA1598'
}

res = requests.get(url,headers = headers)
result = res.content.decode('utf-8')

print(res.content.decode('utf-8'))

reg = r'.*?(本机IP.*?)</span>'
list_result = re.findall(reg,result)

print(list_result)