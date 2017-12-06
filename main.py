# -*- coding:utf-8 -*- 
__author__ = 'wangxuan'

from scrapy.cmdline import execute
import sys
import os

# 项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])