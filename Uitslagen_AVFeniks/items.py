# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WedstrijdItem(scrapy.Item):
    wedstrijd = scrapy.Field()
    datum = scrapy.Field()
    plaats = scrapy.Field()
    categorie = scrapy.Field()


class UitslagenAvfeniksItem(scrapy.Item):
    name = scrapy.Field()


class UitslagenAvfeniksItem(scrapy.Item):
    name = scrapy.Field()


class UitslagenAvfeniksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
