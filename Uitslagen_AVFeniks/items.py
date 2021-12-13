# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WedstrijdItem(scrapy.Item):
    wedstrijd = scrapy.Field()
    datum = scrapy.Field()
    plaats = scrapy.Field()
    onderdeel = scrapy.Field()


class CategorieItem(scrapy.Item):
    onderdeel = scrapy.Field()
    atleet = scrapy.Field()


class AtleetItem(scrapy.Item):
    atleet = scrapy.Field()
    categorie = scrapy.Field()
    uitslag = scrapy.Field()


class UitslagItem(scrapy.Item):
    resultaat = scrapy.Field()
    onderdeel = scrapy.Field()
    wind = scrapy.Field()


class UitslagenAvfeniksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
