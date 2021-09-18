import os 
from pathlib import Path
from threading import Thread
import requests
import urllib
from tenacity import retry, stop_after_attempt, stop_after_delay
from time import time
from queue import Queue

proxies = {
  'http': 'http://127.0.0.1:11223',
  'https': 'http://127.0.0.1:11223',
}
#add your proxy


class downloadworker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            item = self.queue.get()
            if item is None:
                break
            url1, url2, num, dir = item
            downloadv(url1, url2, num,dir)
            self.queue.task_done()
@retry
def downloadv(url1,url2,num,dir):
    url = url1 + num + url2
    r = requests.get(url,proxies=proxies)
    filename = str(url.split('?')[0].split('/')[-1])
    with (Path(dir) / filename).open("wb") as fd:
        fd.write(r.content)
        if 0 < os.path.getsize(dir + filename) < 2000000:
            os.remove(dir + filename)
            downloadv()

def main():
    ts = time()
    queue = Queue()

    filepath = 'D:\\2021-09-06\\'
    dmm = 'D:/dmm/'
    count = []
    count1 = []
    for i in os.walk(filepath):
        for j in i[2][2:-1]:
            size = os.path.getsize(filepath + j)
            if size < 2000000:
                count.append(j.split('_')[-1].split('.')[0])
                # print(j,size)
        # print(i[2][2]) #media_b6000000_0.ts
        # print(len(count))
        # print(count)

    for i in os.walk(dmm):
        for j in i[2]:
            count1.append(j.split('_')[-1].split('.')[0])

    lasturl_num = list(set(count).difference(set(count1)))

    url_1 = 'https://stc017.dmm.com/digital/st1:8bC+5n5X5Jpm1D3e6yuOCno000Ob69AM8OZ32cJkiPYhrlWx3mOzHcp4TaXl85frjBn7Sk9ctg-uWJwkC1j6kA==/TevC77gkar9LqSy9UZdhV6-5372b3aaaeeb123caf82f68145eccacf1630890578/-/media_b6000000_'
    url_2 = '.ts?ld=SfgMiEgM1ZyIsCM3x3sV4pn%2F32aFmm%2B51T%2BAOGa%2Fu9wHBAhaUQQGz5dsClxcf8Df7BsJg4DLkJUc9O3TH2JNwNX1fQgXzSkVkbnB2Ng7MFuZdNGMNs%2B1vOTPHrCzKXNr&amp;luid=cojp'
    
    for x in range(32):
        worker = downloadworker(queue)
        # Setting daemon to True will let the main thread exit even though the
        # workers are blocking
        worker.daemon = True
        worker.start()

    for i in lasturl_num:
        queue.put((url_1,url_2,i,dmm))

    queue.join()
    print('Took {}s'.format(time() - ts))

    # @retry(stop=stop_after_delay(10))
    # def test_retry():
    #     print("等待重试...")
    #     raise Exception

    # test_retry()

if __name__ == '__main__':
    main()

            
