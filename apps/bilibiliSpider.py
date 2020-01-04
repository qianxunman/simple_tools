import requests
import time

print(time.time())

url = 'https://101.75.242.2:443/upgcxcode/89/22/81222289/81222289-1-30280.m4s?expires=1553704800&platform=pc' \
      '&ssig=DF2tQsYFk6DSPO-bvCRuzA&oi=989587978&trid=322825e1f85e4e7d98d08ac8be4a8821&nfb=maPYqpoel5MI3qOUX6YpRA==&nfc=1'

header = {
    'Host': 'cn-hbcd2-cu-v-07.acgvideo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.bilibili.com/video/av46358604?spm_id_from=333.334.b_62696c695f646f756761.7',
    'Range': 'bytes=0-6146825',
    'Origin': 'https://www.bilibili.com',
    'Connection': 'keep-alive',
}

res = requests.get(url, headers=header, verify=False)
print(res.content)

with open('test.mp4','wb') as f:
    f.write(res.content)
