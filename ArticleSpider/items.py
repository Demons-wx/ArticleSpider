# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
from scrapy.loader import ItemLoader
import re
from ArticleSpider.utils.common import extract_num
from ArticleSpider.settings import SQL_DATE_FORMAT, SQL_DATETIME_FORMAT

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date

def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value

def return_value(value):
    return value


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor = MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor = MapCompose(remove_comment_tags),
        output_processor = Join(",")
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                            insert into jobbole_article(title, url, url_object_id, front_image_url, front_image_path, 
                                comment_nums, fav_nums, praise_nums, tags, content, create_date)
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
        params = (self["title"], self["url"], self["url_object_id"], self["front_image_url"],
                  self["front_image_path"], self["comment_nums"], self["fav_nums"],
                  self["praise_nums"], self["tags"], self["content"], self["create_date"])

        return insert_sql, params

class ArticleItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()

class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, content, 
                answer_num, comments_num, watch_user_num, click_num, crawl_time)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num), comments_num=VALUES(comments_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """

        zhihu_id = self["zhihu_id"][0]
        topics = ",".join(self["topics"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = extract_num("".join(self["answer_num"]))
        comments_num = extract_num("".join(self["comments_num"]))
        if len(self["watch_user_num"]) == 2:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            click_num = 0
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)


        params = (zhihu_id, topics, url, title, content,
                answer_num, comments_num, watch_user_num, click_num, crawl_time)

        return insert_sql, params

class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        # 插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, comments_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content), comments_num=VALUES(comments_num), praise_num=VALUES(praise_num),
              update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params

class LagouJob(scrapy.Item):
     title = scrapy.Field()
     url = scrapy.Field()
     url_object_id = scrapy.Field()
     salary = scrapy.Field()
     job_city = scrapy.Field()
     work_years = scrapy.Field()
     degree_need = scrapy.Field()
     job_type = scrapy.Field()
     publish_time = scrapy.Field()
     job_advantage = scrapy.Field()
     job_desc = scrapy.Field()
     job_addr = scrapy.Field()
     company_name = scrapy.Field()
     company_url = scrapy.Field()
     tags = scrapy.Field()
     crawl_time = scrapy.Field()