   
import scrapy
import mysql.connector
from curl_cffi import requests as curl_requests

class CityinfoSpider(scrapy.Spider):
    name = "cityinfo"

    def start_requests(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database="lawinfo_db"
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT state_name, state_url FROM states")
        states = self.cursor.fetchall()
       
        for state_name, state_url in states:

            resp = curl_requests.get(
                state_url,
                impersonate="chrome120",
                headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                # 'if-modified-since': 'Wed, 24 Jun 2026 06:45:52 GMT',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
                'cookie': 'cludo_referrer_url_title=Find Top Social Security Disability Lawyers Near You | LawInfo Attorney Directory; at_check=true; AMCVS_5C64123F5245AF950A490D45%40AdobeOrg=1; AMCV_5C64123F5245AF950A490D45%40AdobeOrg=179643557%7CMCIDTS%7C20629%7CMCMID%7C03404013415899815731346397638575144845%7CMCAAMLH-1782885488%7C12%7CMCAAMB-1782885488%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1782287888s%7CNONE%7CvVersion%7C5.5.0; user_location=eyJsYXRpdHVkZSI6IjE5LjA3MjgzIiwibG9uZ2l0dWRlIjoiNzIuODgyNjEiLCJjaXR5IjoiTXVtYmFpIiwicG9zdGFsQ29kZSI6IjQwMDAxNyIsInJlZ2lvbiI6Ik1haGFyYXNodHJhIiwicmVnaW9uQ29kZSI6Ik1IIiwiY291bnRyeSI6IklOIn0=; cludo_referrer_url_title=Attorneys and Lawyers Directory | Legal Resources | LawInfo; usprivacy=1---; s_vnc365=1813816689673%26vn%3D1; s_ivc=true; s_inv=0; _gcl_au=1.1.899041200.1782280690; _ga=GA1.1.202944621.1782280690; _clck=1pc48r6%5E2%5Eg76%5E0%5E2366; session_lawinfo_prod=bsd9ugdp3ghg5ph0liiehp6edb8tp98i; OptanonAlertBoxClosed=2026-06-24T05:59:19.697Z; _fbp=fb.1.1782281786001.591977989825230785; AWSALBTG=3jI70yfgkWbHvmvgYz/2cP5zS4zmu9BFO4v/Qra6t36GLc7/NDpQpILRvEIIZml7ZehvoBUB1rI54/pQQE/VRq+V/SovKssFxo206/R6QroJbnj72YhM+njZAnTx0p0ubH/bP27Hqv7/t+K0Pez4Nu5bitExeaS5o3qUvZ5Z/Itz; AWSALBTGCORS=3jI70yfgkWbHvmvgYz/2cP5zS4zmu9BFO4v/Qra6t36GLc7/NDpQpILRvEIIZml7ZehvoBUB1rI54/pQQE/VRq+V/SovKssFxo206/R6QroJbnj72YhM+njZAnTx0p0ubH/bP27Hqv7/t+K0Pez4Nu5bitExeaS5o3qUvZ5Z/Itz; gpv_v22=https%3A%2F%2Fwww.lawinfo.com%2Fsocial-security-disability%2F; s_sess=%20s_sq%3D%3B%20s_cc%3Dtrue%3B; fl_last_page_view_id=a109cb97700d85e8; _ga_99KZ6LFRW5=GS2.1.s1782280689$o1$g1$t1782284294$j58$l0$h0; gpv_v12=LI.com%3ALIDirectory%3ALawyerDirectory%3APABrowse%3ATop%20Social%20Security%20Disability%20Lawyers%20Near%20You; __cf_bm=92rmkPYrSscy7Q4A5eabt.PtwKzqxt_iN_BJn.aj6QY-1782285272.34659-1.0.1.1-gkwDlLmdXc92id6UONwjlqZjV1JTRosVr9AbDCU94iXykTWT5j5moUvg0B_IDikPXqvmP5aDtFZFXOYf3a9SIqfUVQ.AKuAAEvzYJlD_qW3W.K0Wzb.MlIQe0SD1zAItVUHY5pJIC3un1ReIZ81m4g; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jun+24+2026+12%3A44%3A38+GMT%2B0530+(India+Standard+Time)&version=202604.2.0&browserGpcFlag=0&isDntEnabled=0&isIABGlobal=false&hosts=&consentId=4703c696-f3a3-4605-b790-a669b4ce011a&interactionCount=1&isAnonUser=1&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&crTime=1782280758964&AwaitingReconsent=false&geolocation=IN%3BMH; mbox=session#71a1f6766f3b4b70a919043ccd46308c#1782287140|PC#71a1f6766f3b4b70a919043ccd46308c.41_0#1845525489; s_nr30=1782285282837-New; s_tslv=1782285282839; invoca_session=%7B%22ttl%22%3A%222026-07-24T07%3A14%3A44.468Z%22%2C%22session%22%3A%7B%22invoca_id%22%3A%22i-da44567f-3fbe-4900-cda5-a59c50854bcd%22%7D%2C%22config%22%3A%7B%22ce%22%3Atrue%2C%22fv%22%3Afalse%2C%22rn%22%3Afalse%2C%22ba%22%3Atrue%2C%22br%22%3Atrue%7D%7D; _clsk=12nfchk%5E1782285284668%5E43%5E1%5Et.clarity.ms%2Fcollect',
            }
            )
            # convert to Scrapy response manually
            response = scrapy.http.HtmlResponse(
                url=state_url,
                body=resp.content,
                encoding="utf-8",
                request=scrapy.Request(state_url, meta={"state": state_name})
            )

            yield from self.parse(response)

    def parse(self, response):
        state = response.meta["state"]

        cities = response.xpath(
            '//h3[starts-with(@id,"letter-")]/following-sibling::ul[1]//a'
        )

        for city in cities:
            yield {
                "state": state,
                "city": city.xpath("./text()").get(),
                "city_url": response.urljoin(city.xpath("./@href").get())
            }

    def closed(self, reason):
        self.cursor.close()
        self.conn.close()