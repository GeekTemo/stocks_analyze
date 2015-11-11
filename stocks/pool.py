# -*- coding:utf-8 -*-
import queue
import multiprocessing


class BrowerPool:
    def __init__(self, nums, call_back):
        self.brower_nums = nums
        self.url_queue = queue.Queue()
        self.call_back = call_back


    def add_url(self, url):
        pass

    def start(self):
        pass