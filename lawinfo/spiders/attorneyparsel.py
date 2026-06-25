import scrapy
import mysql.connector
from curl_cffi import requests as curl_requests


class AttorneyparselSpider(scrapy.Spider):
    name = "attorneyparsel"
    allowed_domains = ["lawinfo.com"]
    start_urls = ["https://lawinfo.com"]

    def parse(self, response):
        pass
    def start_requests(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database="lawinfo_db"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT firm_name, firm_url FROM firms")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        for firm_name, firm_url in rows:
            resp = curl_requests.get(
                firm_url,
                impersonate="chrome120",
                headers={
                    "User-Agent": "Mozilla/5.0 Chrome/120",
                    "Accept": "text/html,application/xhtml+xml",
                    "Referer": firm_url
                }
            )

            if resp.status_code != 200:
                self.logger.warning(f"Blocked {firm_url} -> {resp.status_code}")
                continue

            response = scrapy.http.HtmlResponse(
                url=firm_url,
                body=resp.content,
                encoding="utf-8",
                request=scrapy.Request(firm_url, meta={"firm_name": firm_name})
            )
            yield from self.parse(response)

    def parse(self, response):
        firm_name = response.meta["firm_name"]

        # ===== extract data =====
        job_info = response.xpath(
            '//p[contains(@class,"listing-details-tagline")]//text()'
        ).getall()

        job_info = " ".join([x.strip() for x in job_info if x.strip()])
        
        phone = response.xpath('normalize-space(//a[contains(@href,"tel:")])').get()
        email = response.xpath('//a[contains(@href,"mailto:")]/text()').get()

        street = response.xpath(
            '//p[contains(@class,"listing-desc-address")]//span[@class="street-address"]//text()'
        ).getall()

        street_address = " ".join([x.strip() for x in street if x.strip()])
        
        city_raw = response.xpath('//span[@class="locality"]/text()').get()
        city = city_raw.replace("Serving", "").strip() if city_raw else None

        state = response.xpath(
            '//span[@class="region"]/text()'
        ).get()
        zipcode = response.xpath(
            '//span[@class="postal-code"]/text()'
        ).get()
       
        block = response.xpath('//div[contains(@class,"lc-attorney-record")]')

        lead_counsel_text = response.xpath(
            '//div[@id="lead-counsel-verified"]//text()'
        ).getall()

        lead_counsel_text = " ".join([x.strip() for x in lead_counsel_text if x.strip()])
        lead_counsel_text = lead_counsel_text if lead_counsel_text else "NA"

        if block:

            for b in block:

                name = b.xpath('.//h2[@class="h3"]/text()').get()

                desc = " ".join(
                    b.xpath('.//p[@id="lead_counsel_desc"]//text()').getall()
                ).strip()

                practice_area = b.xpath('.//table//tbody//tr//td[1]//a/text()').get()
                year = b.xpath('.//table//tbody//tr//td[2]//text()').get()
                yield {
                    "atty_firm_name": firm_name if firm_name else "NA",
                    "atty_job_info": job_info,
                    "atty_phone": phone,
                    "atty_email": email,
                    "atty_lawyer_name": name if name else "NA",
                    "atty_description": desc if desc else "NA",
                    "atty_lead_counsel_text": lead_counsel_text,
                    "atty_practice_area": practice_area if practice_area else "NA",
                    "atty_verified_year": year if year else "NA",
                    "atty_street_address": street_address,
                    "atty_city": city,
                    "atty_state": state,
                    "atty_zipcode": zipcode,
                    "atty_firm_url": response.url
                }
        else:
            yield {
                "atty_firm_name": firm_name if firm_name else "NA",
                "atty_job_info": job_info,
                "atty_phone": phone,
                "atty_email": email,
                "atty_lawyer_name": "NA",
                "atty_description": "NA",
                "atty_lead_counsel_text": lead_counsel_text,
                "atty_practice_area": "NA",
                "atty_verified_year": "NA",
                "atty_street_address": street_address,
                "atty_city": city,
                "atty_state": state,
                "atty_zipcode": zipcode,
                "atty_firm_url": response.url
            }