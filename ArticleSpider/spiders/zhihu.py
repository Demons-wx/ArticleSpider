# -*- coding: utf-8 -*-
import scrapy


# 使用命令：scrapy genspider zhihu www.zhihu.com

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass
