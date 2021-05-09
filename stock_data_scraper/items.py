# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class FinvizItem(Item):
    id = Field()
    ticker = Field()
    full_name = Field()
    sector = Field()
    industry = Field()
    country = Field()
    table1 = Field()
    created_at = Field()
