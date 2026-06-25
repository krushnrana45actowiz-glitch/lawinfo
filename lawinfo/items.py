# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LawinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    state_name = scrapy.Field()
    state_url = scrapy.Field()

    city_name = scrapy.Field()
    city_url = scrapy.Field()

    firm_name = scrapy.Field()
    firm_url = scrapy.Field()
    firm_id = scrapy.Field()

    job_info = scrapy.Field() 
    phone = scrapy.Field()
    email = scrapy.Field()

    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()