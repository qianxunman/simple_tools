# author: luojun
# date: 2019/12/27 22:00

import requests
from pprint import pprint
import json
import re


class Train(object):
    def __init__(self):
        self.url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2020-01-25&leftTicketDTO.from_station=SZQ&leftTicketDTO.to_station=ESN&purpose_codes=ADULT'
        self.hearder = {
            "Host": "kyfw.12306.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "If-Modified-Since": "0",
            "Cache-Control": "no-cache",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            # "Referer": "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E6%B7%B1%E5%9C%B3,SZQ&ts=%E6%81%A9%E6%96%BD,ESN&date=2020-01-21&flag=N,N,Y",
            "Cookie": "JSESSIONID=900C9CD4CBE3D754042D774D0BD40996;"

        }

    def get_avaliable_ticket(self, date, station_from='SZQ', station_to='ESN'):
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
            date, station_from, station_to)
        res = requests.get(url=url, headers=self.hearder)

        text = res.content.decode('utf-8')
        json_text = json.loads(text)
        list_record = json_text.get('data').get('result')
        # pprint(json_text)
        # pprint(list_record)
        list_trains_data = []
        for i in list_record:
            dict_trans = {}
            list_data = str(i).split('|')
            # pprint(list_data)
            dict_trans['date'] = date
            dict_trans['tran_no'] = list_data[3]
            # 二等座位置 -15
            dict_trans['site_second'] = list_data[30]
            # 硬座
            dict_trans['sit_hard'] = list_data[29]
            # 软座,看了下软座都没有卖的
            # dict_trans['sit_soft'] = list_data[-17]
            # 软卧
            dict_trans['sleep_soft'] = list_data[23]
            # 硬卧
            dict_trans['sleep_hard'] = list_data[28]
            # dict_trans['no_sit'] = list_data[26]

            if '有' in dict_trans.values() or True in [i.isdigit() for i in dict_trans.values()]:
                list_trains_data.append(dict_trans)

            # 不能将所有的车次信息返回,应该是要返回存在存在余票的数据:
            # for key in dict_trans:
            #     # print(key, dict_trans[key])
            #     if dict_trans[key] == '有' or isinstance(dict_trans[key], int):
            #         pass
            # list_trains_data.append(dict_trans)
            # print(dict_trans.values())
            #

            # pprint(dict_trans)
        print(list_trains_data)
        return list_trains_data


def spider():
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2020-01-25&leftTicketDTO.from_station=SZQ&leftTicketDTO.to_station=ESN&purpose_codes=ADULT'
    # url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ'
    # url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2020-01-25&leftTicketDTO.from_station=ESN&leftTicketDTO.to_station=HAN&purpose_codes=ADULT'

    query = {
        "leftTicketDTO.train_date": "2020-01-21",
        "leftTicketDTO.from_station": "SZQ",
        "leftTicketDTO.to_station": "ESN",
        "purpose_codes": "ADULT"
    }

    header = {
        "Host": "kyfw.12306.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "If-Modified-Since": "0",
        "Cache-Control": "no-cache",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        # "Referer": "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E6%B7%B1%E5%9C%B3,SZQ&ts=%E6%81%A9%E6%96%BD,ESN&date=2020-01-21&flag=N,N,Y",
        "Cookie": "JSESSIONID=900C9CD4CBE3D754042D774D0BD40996;"

    }
    # params = query,
    pprint(query)
    res = requests.get(url, headers=header, )
    text = res.content.decode('utf-8')

    # print(res)
    #
    # pprint(res.url)
    # pprint(res.headers)
    # pprint(dir(res.request.url))
    # pprint(res.request.url)
    # pprint(res.raw.geturl())
    json_text = json.loads(text)
    list_record = json_text.get('data').get('result')
    pprint(json_text)
    pprint(list_record)
    list_trans_data = []
    for i in list_record:
        dict_trans = {}
        list_data = str(i).split('|')
        pprint(list_data)
        dict_trans['date'] = 'rq'
        dict_trans['tran_no'] = list_data[3]
        # 二等座位置 -15
        dict_trans['site_second'] = list_data[30]
        # 硬座
        dict_trans['sit_hard'] = list_data[29]
        # 软座,看了下软座都没有卖的
        # dict_trans['sit_soft'] = list_data[-17]
        # 软卧
        dict_trans['sleep_soft'] = list_data[23]
        # 硬卧
        dict_trans['sleep_hard'] = list_data[28]
        # dict_trans['no_sit'] = list_data[26]

        pprint(dict_trans)


def station_info():
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971"
    response = requests.get(url, verify=False)
    # 将车站的名字和编码进行提取
    chezhan = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
    chezhan_code = dict(chezhan)
    # pprint(chezhan)
    # pprint(chezhan_code)
    # 进行交换
    chezhan_names = dict(zip(chezhan_code.values(), chezhan_code.keys()))
    # 打印出得到的车站字典
    # pprint(chezhan_names)


def main():
    train = Train()
    list_ticket = []
    for i in ['2020-01-21', '2020-01-21', '2020-01-22', '2020-01-23']:
        tickets = train.get_avaliable_ticket(i)
        list_ticket += tickets
    return list_ticket


if __name__ == '__main__':
    # spider()
    # station_info()
    tem = main()
    print(tem)
