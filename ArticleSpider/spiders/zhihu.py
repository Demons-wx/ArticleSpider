# -*- coding: utf-8 -*-

import scrapy
import re
import json
import time
from PIL import Image

# 使用命令：scrapy genspider zhihu www.zhihu.com

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': agent
    }

    xsrf = ""

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin', headers=self.headers, callback=self.get_xsrf)]


    def get_xsrf(self, response):
        response_text = response.text
        # 正则表达式默认只会匹配当前内容的第一行(如果内容中包含换行符，使用re.DOTALL来匹配全文)
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
        if match_obj:
            self.xsrf = (match_obj.group(1))

        # 获取验证码
        t = str(int(time.time() * 1000))
        captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)

        return [scrapy.Request(
            url=captcha_url,
            headers=self.headers,
            callback=self.login
        )]

    def login(self, response):

        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()


        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        if self.xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": self.xsrf,
                "phone_num": "15580205042",
                "password": "www921105",
                "captcha": captcha
            }

            return [scrapy.FormRequest(
                url = post_url,
                formdata = post_data,
                headers = self.headers,
                callback = self.check_login
            )]

    def check_login(self, response):
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                 yield scrapy.Request(url, dont_filter=True, headers=self.headers)
