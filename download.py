import json
import os
import requests

from itertools import chain
from pathlib import Path

from bs4 import BeautifulSoup
import urllib
from tenacity import retry

# 结合 requests 和 bs4 解析出网页中的全部图片链接，返回一个包含全部图片链接的列表
def get_links(url):
    # req = requests.get(url)
    # soup = BeautifulSoup(req.text, "html.parser")
    # return [img.attrs.get('data-src') for img in
    #         soup.find_all('div', class_='img-wrap')
    #         if img.attrs.get('data-src') is not None]

    wbdata = str((requests.get(url).content),'utf-8')
    soup = BeautifulSoup(wbdata,'html.parser')
    title = soup.select("img.outputthumb")
    count = 0
    while(count < 10):
        title.pop()
        count = count + 1 

    link = []

    for inx,val in enumerate(title):
        link.append(val.get("src").split('?')[0])
    return link


#把图片下载到本地
@retry
def download_link(directory, link, name):
    img_name = str(urllib.parse.unquote(os.path.basename(link),'utf-8'))
    # tistory_true_link = str(link.split('+')[0]) + '?original'
    # img_tistory_name = str(link.split('+')[1] + '.jpg')
    # name = '[' + (link.split('/')[-1]).split('?')[1] + ']' + "_" + (link.split('/')[-1]).split('?')[0]
    download_path = directory / name
    # if download_path.exists():
    #     count = count + 1
    #     name = img_name.split('.')
    #     img_name = name[0] + '({})'.format(count) + '.' +name[1]
    #     download_path = directory / img_name
    # proxies = {
    #     'http': 'http://127.0.0.1:11223',
    #     'https': 'http://127.0.0.1:11223',
    # }
    r = requests.get(link)
    with download_path.open('wb') as fd:
        fd.write(r.content)

@retry
def download_link_naver(directory,link):
    img_name = str(urllib.parse.unquote(os.path.basename(link),'utf-8'))
    download_path = directory / img_name
    r = requests.get(link)
    with download_path.open('wb') as fd:
        fd.write(r.content)

# 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建
def setup_download_dir(directory):
    download_dir = Path(directory)
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir

# setup_download_dir("D:/izonedownload")