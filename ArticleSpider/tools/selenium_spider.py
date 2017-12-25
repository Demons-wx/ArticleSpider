# -*- coding:utf-8 -*- 
__author__ = 'wangxuan'

# 安装selenium: pip install selenium

from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Firefox(executable_path="/Users/wangxuan/Downloads/geckodriver")
# browser.get("https://detail.tmall.com/item.htm?spm=875.7931836/B.20161011.1.64bc94afD3RWOd&abtest=_AB-LR845-PR845&pvid=f1ebd772-4928-45d1-9771-d05af4256bfa&pos=1&abbucket=_AB-M845_B9&acm=201509290.1003.1.1286473&id=560597539512&scm=1007.12710.81710.100200300000000&sku_properties=10004:709990523;5919063:6536025;12304035:11835346")
#
# print(browser.page_source)
#
# t_selector = Selector(text=browser.page_source)
# print (t_selector.css(".tm-promo-price .tm-price::text").extract())

browser.get("https://www.zhihu.com/#signin")

browser.find_element_by_css_selector(".SignFlow-accountInput input[name='username']").send_keys("15580205042")
browser.find_element_by_css_selector(".SignFlow-password input[name='password']").send_keys("www921105")
browser.find_element_by_css_selector(".SignFlow-submitButton").click()

# browser.quit()

