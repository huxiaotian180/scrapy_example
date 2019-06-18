# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst

def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date

def get_nums(value):
    match_re = re.match(r".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

def return_value(value):
    return value

def remove_comment_tags(value):
    # 去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()

    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums, front_image_url, front_image_path,
            praise_nums, comment_nums, tags, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """

        fron_image_url = ""
        # content = remove_tags(self["content"])

        if self["front_image_url"]:
            fron_image_url = self["front_image_url"][0]
        params = (
            self["title"],
            self["url"],
            self["create_date"],
            self["fav_nums"],
            fron_image_url,
            self["front_image_path"],
            self["praise_nums"],
            self["comment_nums"],
            self["tags"],
            self["content"])
        return insert_sql, params


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()
