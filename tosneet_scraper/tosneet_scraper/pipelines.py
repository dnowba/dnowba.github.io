# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pathlib import Path


class TosneetScraperPipeline(object):
    def open_spider(self, spider):
        self.htmldir_path = Path('htmls') / spider.name

    def process_item(self, item, spider):
        if spider.pfull_html is not None:
            fname = item['ClassID'] + '.html'
            p = self.htmldir_path / fname
            p.write_bytes(item['html'])
            del item['html']
        return item
