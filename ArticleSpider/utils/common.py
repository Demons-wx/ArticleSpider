# -*- coding:utf-8 -*- 
__author__ = 'wangxuan'

import hashlib

def get_md5(url):

    # md5不支持对unicode进行加密，需要将unicode字符串转成utf-8
    if isinstance(url, str):
        url = url.encode("utf-8")

    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    print (get_md5("http://jobbole.com".encode("utf-8")))