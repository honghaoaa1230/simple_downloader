import os
from queue import Queue
from threading import Thread
from time import time
from itertools import chain
import string

from download import setup_download_dir, get_links, download_link, download_link_naver
# from pickit_izone_card import get_link
import datetime
import requests
import urllib
import json
# import copy

class DownloadWorker_pin(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            item = self.queue.get()
            if item is None:
                break
            directory, link, name = item
            download_link(directory, link, name)
            self.queue.task_done()

class DownloadWorker_naver(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            item = self.queue.get()
            if item is None:
                break
            directory, link = item
            download_link_naver(directory, link)
            self.queue.task_done()

def main():
    ts = time()
    website = input("website[1.naver|2.pinterest]: ")

    path = str(datetime.date.today())
    download_dir = setup_download_dir('D:/'+ path)
    # Create a queue to communicate with the worker threads
    queue = Queue()
    count = 0

    if website == '2':
        filelocation = input("file absolute location:")
        with open(filelocation,'r',encoding='UTF-8') as f:
            data = json.load(f)
        
        count = len(data)
        # 8 Threads,92s; 16 Threads,51s; 32Threads,26s; 64 Threads,18s; date:190504 0:36
        for x in range(32):
            worker = DownloadWorker_pin(queue)
            # Setting daemon to True will let the main thread exit even though the
            # workers are blocking
            worker.daemon = True
            worker.start()
        # Put the tasks into the queue as a tuple
        for index in range(len(data)):
            link = str(data[index]["url"])

            latin_letter_small = list("ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘʀsᴛᴜᴠᴡxʏᴢ")
            alphabet_string = list(string.ascii_uppercase)
            alphabet_string.remove("Q")
            diction = dict(zip(latin_letter_small,alphabet_string))
            prename = str(data[index]["name"])
            realname = ''
            for ch in prename:
                if ch in latin_letter_small:
                    realname += diction[ch]
                else:
                    realname += ch

            name = str(index) + '_' + realname + '.jpg'
            queue.put((download_dir, link, name))
    else:
        from naver import get_link

        count = len(get_link())

        for x in range(32):
            worker = DownloadWorker_naver(queue)
            # Setting daemon to True will let the main thread exit even though the
            # workers are blocking
            worker.daemon = True
            worker.start()
        
        for link in get_link():
            queue.put((download_dir, link))
    # Causes the main thread to wait for the queue to finish processing all
    # the tasks
    queue.join()
    print('一共下载了 {} 张图片'.format(count))
    print('Took {}s'.format(time() - ts))


if __name__ == '__main__':
    main()