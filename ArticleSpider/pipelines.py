# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 可用来做数据存储

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import codecs
import json
import MySQLdb
import MySQLdb.cursors

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

# 将item写入json文件
class jsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        # 第二个参数ensure_ascii=False是为了防止中文显示不正常
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    # 当spider关闭的时候，这个函数将被调用
    def spider_closed(self, spider):
        self.file.close()

# 将数据存储到mysql (同步插入机制，会影响爬取性能)
# 需要事先安装mysqlclient pip install mysqlclient
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('host', 'user', 'password', 'dbname',
                                    charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, url_object_id, front_image_url, front_image_path, 
                comment_nums, fav_nums, praise_nums, tags, content, create_date)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["url_object_id"], item["front_image_url"],
                                         item["front_image_path"], item["comment_nums"], item["fav_nums"],
                                         item["praise_nums"], item["tags"], item["content"], item["create_date"]))
        self.conn.commit()


# mysql插入异步化
class MysqlTwistedPipline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset = "utf8",
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    # 使用twisted将mysql插入变成异步执行
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error)


    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    # 执行具体地插入
    def do_insert(self, cursor, item):
        insert_sql = """
                    insert into jobbole_article(title, url, url_object_id, front_image_url, front_image_path, 
                        comment_nums, fav_nums, praise_nums, tags, content, create_date)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item["title"], item["url"], item["url_object_id"], item["front_image_url"],
                                         item["front_image_path"], item["comment_nums"], item["fav_nums"],
                                         item["praise_nums"], item["tags"], item["content"], item["create_date"]))


class JsonExporterPipeline(object):
    # 调用scripy提供的json export导出json文件
    def __init__(self):
         self.file = open('articleexport.json', 'wb')
         self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
         self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# 获取下载的图片的路径
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item