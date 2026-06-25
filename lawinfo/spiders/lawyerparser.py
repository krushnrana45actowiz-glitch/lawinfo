# # import scrapy


# # class LawyerparserSpider(scrapy.Spider):
# #     name = "lawyerparser"
# #     allowed_domains = ["lawinfo.com"]
# #     start_urls = ["https://lawinfo.com"]

# #     def parse(self, response):
# #         pass

# import scrapy
# import mysql.connector
# from curl_cffi import requests as curl_requests


# class LawyerparserSpider(scrapy.Spider):
#     name = "lawyerparser"
#     allowed_domains = ["lawinfo.com"]

#     def start_requests(self):
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="actowiz",
#             database="lawinfo_db"
#         )
#         cursor = conn.cursor()

#         cursor.execute("SELECT firm_name, firm_url FROM firms")
#         rows = cursor.fetchall()

#         cursor.close()
#         conn.close()

#         for firm_name, firm_url in rows:
#             resp = curl_requests.get(
#                 firm_url,
#                 impersonate="chrome120",
#                 headers={
#                     "User-Agent": "Mozilla/5.0 Chrome/120",
#                     "Accept": "text/html,application/xhtml+xml",
#                     "Referer": firm_url
#                 }
#             )

#             if resp.status_code != 200:
#                 self.logger.warning(f"Blocked {firm_url} -> {resp.status_code}")
#                 continue

#             response = scrapy.http.HtmlResponse(
#                 url=firm_url,
#                 body=resp.content,
#                 encoding="utf-8",
#                 request=scrapy.Request(firm_url, meta={"firm_name": firm_name})
#             )
#             yield from self.parse(response)

#     def parse(self, response):
#         firm_name = response.meta["firm_name"]

#         # ===== extract data =====
#         job_info = response.xpath(
#             '//p[contains(@class,"listing-details-tagline")]//text()'
#         ).getall()

#         job_info = " ".join([x.strip() for x in job_info if x.strip()])
        
#         phone = response.xpath('normalize-space(//a[contains(@href,"tel:")])').get()
#         email = response.xpath('//a[contains(@href,"mailto:")]/text()').get()

#         street = response.xpath(
#             '//p[contains(@class,"listing-desc-address")]//span[@class="street-address"]//text()'
#         ).getall()

#         street_address = " ".join([x.strip() for x in street if x.strip()])
        
#         city_raw = response.xpath('//span[@class="locality"]/text()').get()
#         city = city_raw.replace("Serving", "").strip() if city_raw else None

#         state = response.xpath(
#             '//span[@class="region"]/text()'
#         ).get()
#         zipcode = response.xpath(
#             '//span[@class="postal-code"]/text()'
#         ).get()

#         block = response.xpath('//div[contains(@class,"lc-attorney-record")]')

#         lead_counsel_text = response.xpath(
#             '//div[@id="lead-counsel-verified"]//text()'
#         ).getall()

#         lead_counsel_text = " ".join([x.strip() for x in lead_counsel_text if x.strip()])
#         lead_counsel_text = lead_counsel_text if lead_counsel_text else "NA"

#         if block:

#             for b in block:

#                 name = b.xpath('.//h2[@class="h3"]/text()').get()

#                 desc = " ".join(
#                     b.xpath('.//p[@id="lead_counsel_desc"]//text()').getall()
#                 ).strip()

#                 practice_area = b.xpath('.//table//tbody//tr//td[1]//a/text()').get()
#                 year = b.xpath('.//table//tbody//tr//td[2]//text()').get()
#                 yield {
#                     "firm_name": firm_name if firm_name else "NA",
#                     "job_info": job_info if job_info else "NA",
#                     "phone": phone if phone else "NA",
#                     "email": email if email else "NA",
#                     "name": name if name else "NA",
#                     "description": desc if desc else "NA",
#                     "lead_counsel_text": lead_counsel_text,
#                     "practice_area": practice_area if practice_area else "NA",
#                     "year": year if year else "NA",
#                     "street_address": street_address if street_address else "NA",
#                     "city": city if city else "NA",
#                     "state": state if state else "NA",
#                     "zipcode": zipcode if zipcode else "NA",
#                     "url": response.url
#                     }
#         else:
#             yield {
#                 "firm_name": firm_name if firm_name else "NA",
#                 "job_info": job_info if job_info else "NA",
#                 "phone": phone if phone else "NA",
#                 "email": email if email else "NA",
#                 "name": "NA",
#                 "description": "NA",
#                 "lead_counsel_text": lead_counsel_text,
#                 "practice_area": "NA",
#                 "year": "NA",
#                 "street_address": street_address if street_address else "NA",
#                 "city": city if city else "NA",
#                 "state": state if state else "NA",
#                 "zipcode": zipcode if zipcode else "NA",
#                 "url": response.url
#             }    


import mysql.connector
import scrapy


class LawyerparserSpider(scrapy.Spider):
    name = "lawyerparser"
    allowed_domains = ["lawinfo.com"]

    custom_settings = {
        # 1. Correct import paths for the download handlers
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_curl_cffi.handler.CurlCffiDownloadHandler",
            "https": "scrapy_curl_cffi.handler.CurlCffiDownloadHandler",
        },
        
        # 2. REQUIRED: Include scrapy-curl-cffi's internal middlewares
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_curl_cffi.middlewares.CurlCffiMiddleware": 200,
            "scrapy_curl_cffi.middlewares.DefaultHeadersMiddleware": 400,
        },
        
        "CONCURRENT_REQUESTS": 16,
        "RETRY_TIMES": 3,
        "COOKIES_ENABLED": False,
    }

    def start_requests(self):
        conn = mysql.connector.connect(
            host="localhost", user="root", password="actowiz", database="lawinfo_db"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT firm_name, firm_url FROM firms")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for firm_name, firm_url in rows:
            yield scrapy.Request(
                url=firm_url,
                callback=self.parse,
                # 3. Note: scrapy-curl-cffi reads configuration from 'curl_cffi_options'
                meta={
                    "firm_name": firm_name,
                    "curl_cffi_options": {
                        "impersonate": "chrome120",
                        "verify": False
                    },
                    "headers": {
                        "User-Agent": "Mozilla/5.0 Chrome/120",
                        "Accept": "text/html,application/xhtml+xml",
                        "Referer": firm_url,
                    }
                },
                dont_filter=True,
            )

    def parse(self, response):
        if response.status != 200:
            self.logger.warning(f"Blocked {response.url} -> {response.status}")
            return

        firm_name = response.meta["firm_name"]

        # ===== extract data =====
        job_info = response.xpath(
            '//p[contains(@class,"listing-details-tagline")]//text()'
        ).getall()
        job_info = " ".join([x.strip() for x in job_info if x.strip()])

        phone = response.xpath(
            'normalize-space(//a[contains(@href,"tel:")])'
        ).get()
        email = response.xpath('//a[contains(@href,"mailto:")]/text()').get()

        street = response.xpath(
            '//p[contains(@class,"listing-desc-address")]//span[@class="street-address"]//text()'
        ).getall()
        street_address = " ".join([x.strip() for x in street if x.strip()])

        city_raw = response.xpath('//span[@class="locality"]/text()').get()
        city = city_raw.replace("Serving", "").strip() if city_raw else None

        state = response.xpath('//span[@class="region"]/text()').get()
        zipcode = response.xpath('//span[@class="postal-code"]/text()').get()

        block = response.xpath('//div[contains(@class,"lc-attorney-record")]')

        lead_counsel_text = response.xpath(
            '//div[@id="lead-counsel-verified"]//text()'
        ).getall()
        lead_counsel_text = " ".join(
            [x.strip() for x in lead_counsel_text if x.strip()]
        )
        lead_counsel_text = lead_counsel_text if lead_counsel_text else "NA"

        if block:
            for b in block:
                name = b.xpath('.//h2[@class="h3"]/text()').get()
                desc = " ".join(
                    b.xpath('.//p[@id="lead_counsel_desc"]//text()').getall()
                ).strip()
                practice_area = b.xpath(
                    './/table//tbody//tr//td[1]//a/text()'
                ).get()
                year = b.xpath('.//table//tbody//tr//td[2]//text()').get()

                yield {
                    "firm_name": firm_name if firm_name else "NA",
                    "job_info": job_info if job_info else "NA",
                    "phone": phone if phone else "NA",
                    "email": email if email else "NA",
                    "name": name if name else "NA",
                    "description": desc if desc else "NA",
                    "lead_counsel_text": lead_counsel_text,
                    "practice_area": (
                        practice_area if practice_area else "NA"
                    ),
                    "year": year if year else "NA",
                    "street_address": (
                        street_address if street_address else "NA"
                    ),
                    "city": city if city else "NA",
                    "state": state if state else "NA",
                    "zipcode": zipcode if zipcode else "NA",
                    "url": response.url,
                }
        else:
            yield {
                "firm_name": firm_name if firm_name else "NA",
                "job_info": job_info if job_info else "NA",
                "phone": phone if phone else "NA",
                "email": email if email else "NA",
                "name": "NA",
                "description": "NA",
                "lead_counsel_text": lead_counsel_text,
                "practice_area": "NA",
                "year": "NA",
                "street_address": street_address if street_address else "NA",
                "city": city if city else "NA",
                "state": state if state else "NA",
                "zipcode": zipcode if zipcode else "NA",
                "url": response.url,
            }