#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import re
import threading
import time
import queue
import sys
import importlib

importlib.reload(sys)
_DATA = []
FILE_LOCK = threading.Lock()
SHARE_Q = queue.Queue()
_WORKER_THREAD_NUM = 3


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.func()


def worker():
    global SHARE_Q
    while not SHARE_Q.empty():
        url = SHARE_Q.get()
        my_page = get_page(url)
        find_title(my_page)
        time.sleep(1)
        SHARE_Q.task_done()


def get_page(url):
    try:
        my_page = urllib.request.urlopen(url).read().decode("utf-8")
    except urllib.request.URLError as e:
        if hasattr(e, "code"):
            print("The server couldn't fulfill the request.")
            print("Error code: %s" % e.code)
        elif hasattr(e, "reason"):
            print("We failed to reach a server. Please check your url and read the Reason")
            print("Reason: %s" % e.reason)
    return my_page


def find_title(my_page):
    temp_data = []
    movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
    for index, item in enumerate(movie_items):
        if item.find("&nbsp") == -1:
            temp_data.append(item)
    _DATA.append(temp_data)


def main():
    global SHARE_Q
    threads = []
    douban_url = "http://movie.douban.com/top250?start={page}&filter=&type="
    # 向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
    for index in range(10):
        SHARE_Q.put(douban_url.format(page=index * 25))
    for i in range(_WORKER_THREAD_NUM):
        thread = MyThread(worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    SHARE_Q.join()
    with open("movie.txt", "w+", encoding='utf-8') as my_file:
        for page in _DATA:
            for movie_name in page:
                my_file.write(movie_name + "\n")
    print("Spider Successful!!!")


if __name__ == '__main__':
    main()
