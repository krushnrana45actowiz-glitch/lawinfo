import scrapy
import mysql.connector
from curl_cffi import requests as curl_requests
# class LawyerSpider(scrapy.Spider):
#     name = "lawyer"
#     allowed_domains = ["lawinfo.com"]
#     start_urls = ["https://lawinfo.com"]

#     def parse(self, response):
#         pass

class LawyerSpider(scrapy.Spider):
    name = "lawyerinfo"

    def start_requests(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database="lawinfo_db"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT city_name, city_url FROM cities")
        rows = cursor.fetchall()

        for city_name, city_url in rows:
            resp = curl_requests.get(
                city_url,
                impersonate="chrome120",
                headers={
                    "User-Agent": "Mozilla/5.0 Chrome/120",
                    "Accept": "text/html,application/xhtml+xml",
                    "Referer": city_url
                }
            )

            if resp.status_code != 200:
                self.logger.warning(f"Blocked {city_url} -> {resp.status_code}")
                continue

            response = scrapy.http.HtmlResponse(
                url=city_url,
                body=resp.content,
                encoding="utf-8",
                request=scrapy.Request(city_url, meta={"city": city_name})
            )
            yield from self.parse_lawyers(response)

        cursor.close()
        conn.close()

    def parse_lawyers(self, response):
        city = response.meta["city"]
        cards = response.xpath('//div[contains(@class,"card firm")]')
        
        for card in cards:
            name = card.xpath('.//h2//a/text()').get()
            url = card.xpath('.//h2//a/@href').get()

            if not url:
                continue

            firm_id = url.split("/lawfirm/")[-1].split("/")[-1]

            item = {
                "city": city,
                "firm_name": name,
                "firm_url": url,
                "firm_id": firm_id
            }

            print(item)

            yield item
