#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Administrator'

import re, requests
import time

import random

# 使用类封装每一次请求实例
class GetBeauTyTelPhone(object):
    """
    Base Usage:
    """
    avaliable_phone = []

    def __init__(self, count):
        # :count 请求URL的次数
        self.count = count
        self.url_list = []
        self.header = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cookie': 'UID=vn13SQQzogL3ByJ5Goe0ZjLiVbPR3aVB; gipgeo=51|540; ALBC_CD=c1c234d6-58e5-4f81-a2c7-000b7ce317e5; WT.mc_id=guangdong_ADKS_1708_sogouwap_3d14859e78af0841; mallcity=51|510; userprocode=051; citycode=510; _n3fa_cid=0971afd274b341a0ab027f7bae4ba52b; _n3fa_ext=ft=1550228959; _n3fa_lvt_a9e72dfe4a54a20c3d6e671b3bad01d9=1550228959; _n3fa_lpvt_a9e72dfe4a54a20c3d6e671b3bad01d9=1550228989; WT_FPC=id=26dd445034e78b230981550228732503:lv=1550229044200:ss=1550228732503; ALOBNC_CD=df82eb2b-7ff6-4f5a-b13e-c912545088c1; JSESSIONID=563w2g8rEyzux0-xpK1XBzSBrFLy7nPFVai2doUbPuuOT4O01G22!1555105517; SHOP_PROV_CITY='

        }
        self.HTTPResponse = ''
        self.res_reg = r'.*numArray\":\[(.*?)\],\"'
        # 用来存放手机号
        self.telephone = []
        self.pick_telephone = []

    def final_call(self):
        """
        获取请求的URL地址列表
        :return:
        """
        self.start_Num = 1550229044070
        self.end_num = self.start_Num + self.count
        for i in range(self.start_Num, self.end_num, 1):
            print('正在获取第%d批次数据'%(i))
            temp_url = 'https://m.10010.com/NumApp/NumberCenter/qryNum?callback=jsonp_queryMoreNums&provinceCode=51&cityCode=540&monthFeeLimit=0&groupKey=7100388009&searchCategory=3&net=01&amounts=200&codeTypeCode=&searchValue=&qryType=02&goodsNet=4&_=%d' % (
                i)
            self.url_list.append(temp_url)
            try:
                self.requestURL(temp_url)
                self.write_to_file('\n'.join(self.telephone), str(self.start_Num) + '_' + str(self.end_num) + '.txt')
            except:
                print('error request:%d'%(i))
                time.sleep(120)
                continue
            time.sleep(5)

        print(self.telephone)
        self.choose_telephone()






    def requestURL(self, url):
        self.HTTPResponse = requests.get(url, headers=self.header).content.decode('utf-8')
        # print(self.HTTPResponse)
        self.get_all_telphone(self.HTTPResponse)

    def get_all_telphone(self,HTTPResponse):
        """
        获取正常的电话号码列表
        :return: 手机号列表
        """
        result = re.findall(self.res_reg, HTTPResponse)[0]
        result = result.split(',')
        # print(type(result))
        # print(result)
        # print(type(result))
        # print(result)
        for i in result:
            if int(i) > 1:
                self.telephone.append(i)
        # return self.telephone
        # self.write_to_file(str(self.telephone))
        # print(self.telephone)
        # self.choose_telephone()

    def choose_telephone(self):
        """
        根据68原则筛选手机号
        :return: 返回筛选后的手机号列表
        """
        for i in self.telephone:
            if '4' in str(i)[3:] or '7' in str(i)[3:]:
                pass
            else:
                self.pick_telephone.append(i)
                # pass
        print(self.pick_telephone)

    def write_to_file(self,value,filename):
        with open(filename,'a') as f:
            f.write(value)



def main():
    tel = GetBeauTyTelPhone(500)
    tel.final_call()


# 1,拼接请求地址,需要定义一个函数
# 2,cookie是固定的
# 3,请求并获取结果,要多次请求,就会有多个拼接的地址
#   3.1, 需要请求多少数据..
# 4,将结果处理并得到电话号码列表
# 5,根据取86去47原则得到更新的电话号码..
#
# 备注:请求时注意延时:time.sleep(5)


if __name__ == '__main__':
    main()
