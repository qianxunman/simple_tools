# author: luojun
# date: 2020/1/2 23:56

# 多线程的简单实现:

import threading
import time
from queue import Queue
import requests
import logging

logging.basicConfig(level=logging.INFO)


class TestThread(threading.Thread):
    def __init__(self, name, queue):
        super().__init__()
        self.name = name
        self.queue = queue
        self.url = 'http://qianxunman.xyz:9999/'
        self.url2 = 'http://hy.kingtrans.net'
        self.url3 = 'http://120.197.23.190/web'

    def run(self):
        while True:
            if self.queue.empty():
                break
            # res = requests.get(self.url3)
            res = self.qianxun_test()
            logging.info('当前线程:{},当前数据:{},请求结果:{}'.format(self.name, self.queue.get(), res))

            time.sleep(1)
        pass

    def qianxun_test(self):
        url = 'http://qianxunman.xyz:9999/web/dataset/search_read'
        headers = {
            'Host': 'qianxunman.xyz:9999',
            'Connection': 'keep-alive',
            'Content-Length': '326',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://qianxunman.xyz:9999',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0',
            'Content-Type': 'application/json',
            'Referer': 'http://qianxunman.xyz:9999/web?',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'frontend_lang=zh_CN; session_id=96f549341d20114f36874d7c0bb5d0b65099fa3c'
        }
        data = {"jsonrpc": "2.0", "method": "call", "params": {"model": "trans.order_lines", "domain": [],
                                                               "fields": ["order_no", "customer", "location_dest",
                                                                          "amount", "location", "description",
                                                                          "create_time_trans", "is_informed",
                                                                          "date_informed", "create_date", "create_uid"],
                                                               "limit": 80, "sort": "",
                                                               "context": {"tz": False, "lang": "zh_CN", "uid": 2}},
                "id": 174751753}
        res = requests.post(url=url, headers=headers, json=data)
        # logging.info(res)
        return res

    """
'Host': 'qianxunman.xyz:9999',
'Connection': 'keep-alive',
'Content-Length': '326',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Origin': 'http://qianxunman.xyz:9999',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0',
'Content-Type': 'application/json',
'Referer': 'http://qianxunman.xyz:9999/web?',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
"""


def main():
    # 要将100个数字数完,用10个人,每个人数数的间隔为1秒,多久能数完
    count = Queue()
    for i in range(10000):
        count.put(i)

    list_threading = [str(i) for i in range(50)]

    list_instance = []
    for thread_name in list_threading:
        new_thread = TestThread(thread_name, count)
        list_instance.append(new_thread)

    for instance in list_instance:
        instance.start()

    for instance_stop in list_instance:
        instance_stop.join()


if __name__ == '__main__':
    main()
