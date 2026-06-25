import scrapy


class LawyerdetailSpider(scrapy.Spider):
    name = "lawyerdetail"
    allowed_domains = ["lawinfo.com"]
    start_urls = ["https://lawinfo.com"]

    def parse(self, response):
        pass
