
from bs4 import BeautifulSoup
import requests
from itertools import chain
import os
import datetime
import urllib
from pathlib import Path
from time import time
from threading import Thread
from collections import Counter
# from pyaria2 import Jsonrpc
from download import setup_download_dir

# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1088)
# socket.socket = socks.socksocket
# print(requests.get('http://ifconfig.me/ip').text)

# def task(link):
#     img_name = str(urllib.parse.unquote(os.path.basename(link),'utf-8'))
#     download_path = directory / img_name
#     global count
#     if download_path.exists():
#         count = count + 1
#         name = img_name.split('.')
#         img_name = name[0] + '({})'.format(count) + '.' +name[1]
#         download_path = directory / img_name
#         print('file exist! Already rename!')
#     else:
#         print('clear!')
#     print(download_path)
#     r = requests.get(link)
#     with download_path.open('wb') as f:
#             f.write(r.content)

# if __name__ == '__main__':

# proxies = {
#   'http': 'http://127.0.0.1:11223',
#   'https': 'http://127.0.0.1:11223',
# }
url = input("url:")
wbdata = str((requests.get(url).content),'utf-8')
# soup = BeautifulSoup(navertext.html,'html.parser')
# with open('data.txt','w',encoding='utf-8') as f:
#     f.write(wbdata)
html = ''
count = 0
for lines in wbdata.splitlines():
    count += 1
    if count> 150:
        html = html + lines + '\n'
    else:
        continue
soup1 = BeautifulSoup(html,'lxml')
# with open('data_soup.txt','w',encoding='utf-8') as f:
#     f.write(str(soup1))

res = soup1.select(".se_mediaImage")
# res = soup1.find_all("img",class_="se_mediaImage")
links =[]
filename_list = []
for link in res:
    url = link.get("data-src").split('?')[0]
    links.append( url )
    filename_list.append(str(urllib.parse.unquote(os.path.basename(url),'utf-8')))
print(len(res))


# repeated_name = dict(Counter(filename_list))
# repeated_name_list = list({key for key,value in repeated_name.items()if value > 1})
# for name in repeated_name_list:
#     index = list(i for i,x in enumerate(filename_list) if x == name)[1]
#     filename_list[index]  = filename_list[index].split('.')[0] + '(1).jpg'
# # print(filename_list)
# print(len(filename_list))
# dictionary = dict(zip(links,filename_list))

def get_link():
    return links

# path = str(datetime.date.today())
# download_dir = setup_download_dir('D:/'+ path)
# jsonrpc = Jsonrpc('localhost', 6800)
# count = 1
# for link in links:
#     resp = jsonrpc.addUris(link, options={"dir":str(download_dir)})
#     print(resp+' '+str(count))
#     count += 1
    # download_path = download_dir / dictionary[link]
    # r = requests.get(link)
    # with download_path.open('wb') as fd:
    #     fd.write(r.content)

# for url,name in links,filename_list:
#     print(url+'+'+name)
# ab_list = ['a','b','c','a','b']
# print (list(i for i,x in enumerate(ab_list) if x == 'a')[1])
# directory = Path('D:/' + str(datetime.date.today()))
# print(directory)

# piclink = 'https://post-phinf.pstatic.net/MjAyMDA2MjNfMTk5/MDAxNTkyODkwMjAyMTM2.pCP4C4asLrFEJA3X_1Iot5PfMkjHR4FjJOyL0Sjh70kg.hgH97E_U4jlOYb1R9kya_7IisTznHSKyGOGzQQlA_Nsg.JPEG/%EC%9C%A0%EC%A7%843.jpg'
# img_name = os.path.basename(piclink)
# img_name_true = str(urllib.parse.unquote(img_name,'utf-8'))
# print('img_name: ' + img_name_true)
# download_path = directory / img_name_true
# print(download_path)
# ts = time()
# count = 0
# for link in links:
#     task(link)

# print('Took {}s'.format(time() - ts))
