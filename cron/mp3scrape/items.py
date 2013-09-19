# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Mp3ScrapeItem(Item):
    # define the fields for your item here like:
    name = Field()
    remote_url = Field()
    date = Field()
    local_path = Field()
    id3_title = Field()
    id3_artist = Field()
    local_url = Field()
    source = Field()
