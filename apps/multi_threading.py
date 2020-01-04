# author: luojun
# date: 2020/1/2 23:11

# author: luojun
# date: 2019/12/25 23:41

import threading
import requests
from queue import Queue
import time


class Test(threading.Thread):

    def __init__(self, name, page_queue):
        super().__init__()
        self.name = name
        self.page_queue = page_queue

    def run(self):
        print('%s----线程启动' % self.name)
        while 1:
            if self.page_queue.empty():
                break
            print(self.page_queue.get())

        time.sleep(10)
        # while 1:
        #     # 判断采集线程何时退出
        #     if self.page_queue.empty():
        #         break
        #     # 从队列中取出页码
        #     page = self.page_queue.get()
        #     # 拼接url，发送请求
        #     url = self.url.format(page)
        #     r = requests.get(url, headers=self.headers)
        #     # 响应内容存放到data_queue中
        #     self.data_queue.put(r.text)
        print('%s----线程结束' % self.name)


# 创建队列
def create_queue():
    # 创建页码队列
    page_queue = Queue()
    for page in range(1, 500):
        page_queue.put(page)
    # 创建内容队列
    data_queue = Queue()
    return page_queue, data_queue


def main():
    list_tasks = ['thread 1', 'thread 2', 'thread 3', 'thread 4', 'thread 5', ]
    list_thread = []
    time1 = time.time()
    page_queue, data_queue = create_queue()
    for task_name in list_tasks:
        t = Test(task_name, page_queue)
        list_thread.append(t)

    for thread in list_thread:
        thread.start()
    for thread in list_thread:
        thread.join()
    time2 = time.time()
    print(time2 - time1)


if __name__ == '__main__':
    main()
