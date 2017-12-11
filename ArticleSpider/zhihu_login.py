# -*- coding: utf-8 -*-  
__author__ = "wangxuan"

import http.cookiejar as cookielib
import urllib.request
import urllib.parse
import time

url_start = 'https://www.zhihu.com/topic/19556498/questions?page='
cj = cookielib.CookieJar()

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')]

def login():
    username = '15580205042'
    password = 'www921105'
    t = str(int(time.time() * 1000))
    cap_url = 'https://www.zhihu.com/captcha.gif?r='+t+'&type=login'
    cap_content = urllib.request.urlopen(cap_url).read()
    cap_file = open('images/cap.gif', 'wb')
    cap_file.write(cap_content)
    cap_file.close()
    captcha = input('capture:')
    url = 'https://www.zhihu.com/login/phone_num'
    data = urllib.parse.urlencode({"phone_num":username, "password":password, "captcha":captcha}).encode("utf-8")
    print(urllib.request.urlopen(url, data).read())

if __name__ == "__main__":
    login()




