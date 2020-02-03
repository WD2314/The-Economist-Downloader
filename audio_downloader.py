#!/usr/bin/env python3
# -*- coding: utf-8-*-


#import os
from urllib.request import urlopen
from urllib.error import HTTPError
import requests
from tqdm import tqdm


def download_from_url(url, name):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    dst = name
    file_size = int(urlopen(url).info().get('Content-Length', -1))

    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        print('\t'+ dst + ' 已存在，将不再下载')
        return False
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    #print(req.content)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return True

#print("参考网址为：http://audiocdn.economist.com/sites/default/files/AudioArchive/2020/20200125/Issue_9178_20200125_The_Economist_Full_edition.zip\n")

#print("参考日期及期数\n\t20181124\n\t9119")
#print("参考日期及期数\n\t20190330\n\t9136")
print("参考日期及期数\n\t20200125\n\t9178")
print("一周一刊自行推算，期数不对就左右加减，一般向下减\n")

Date = input("请输入文章日期？")
Year = Date[:3]
Num = input("请输入文章期数？")
name = "Issue_" + Num + "_" + Date + "_The_Economist_Full_edition.zip"
#name2 = "Issue_" + Num + "_" + Date + "_The_Economist_Full_Edition.zip" #e or E
url = "http://audiocdn.economist.com/sites/default/files/AudioArchive/" + Year + "/" + Date + "/" + name
#url2 = "http://audiocdn.economist.com/sites/default/files/AudioArchive/" + Year + "/" + Date + "/" + name2

try:
    download_from_url(url, name)
    print("已下载\t"+ name)
    os.system("pause")
except HTTPError as e:
    print(e)
    print("\t请检查日期及期数")
    os.system("pause")

os.system("pause")
