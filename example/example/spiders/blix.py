# -*- coding: utf-8 -*-
from urllib import parse
import scrapy
from scrapy import Request
from example.items import ArticleItemLoader, JobBoleArticleItem
from example.utils.commit.md5 import get_md5

from scrapy.linkextractors import LinkExtractor


class BlixSpider(scrapy.Spider):
    name = 'blix'
    allowed_domains = ["books.toscrape.com"]
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        link = LinkExtractor(restrict_xpaths='//*')
        links = link.extract_links(response)
        print(links)