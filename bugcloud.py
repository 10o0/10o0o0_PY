#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 15:52:59 2018
@author: root
"""
import requests
import time
import datetime
import os
import re
import random

headers = {
    'accept': 'application/json, text/plain, */*',
    'Host': '192.168.2.199',
    'Referer': 'http://192.168.2.199/',
    'cookie': 'sessionid=47rrrukxr4gf0dva18ksu9cxoiny9ea8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0',
}

def get_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        os.makedirs(path)
        print("OK")
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print("False")
        return False
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
def savefile(atype,aname,bugname,bugcode):
    file = os.path.join(atype,aname)
    mkdir(file)
    file = file + '\\'
    print(file)
    with open(file + bugname, 'a+') as f:
        f.write(bugcode)


if __name__ == '__main__':
    page = 0

    while (1):
        page = page + 1
        url = "http://192.168.2.199/cloud/pluginvuln/?page=" + str(page)
        print(url)
        time.sleep(random.randint(1,10))
        json_dict = get_page(url)
#        print(json_dict)
        items = json_dict['results']
        for item in items:
            title = item['plugin']['title']
            code = item['plugin']['source_code']
            type = item['vtype']
            appname = item['fp_app_name']
            newtitle = validateTitle(title)
            try:
                savefile(str(type),str(appname),str(newtitle),code)
            except Exception as e:
                cotent = str(type) + str(appname) + str(newtitle)
                with open("error.txt", 'a+') as f:
                    f.write(cotent)
                continue
            print(title,type,appname)
