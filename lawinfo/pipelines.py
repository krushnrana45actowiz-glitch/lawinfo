# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# from itemadapter import ItemAdapter
# import mysql.connector


# class LawinfoPipeline:

#     def open_spider(self, spider):
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="actowiz",
#             database="lawinfo_db"
#         )
#         self.cursor = self.conn.cursor()

#         # STATES TABLE
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS states (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 state_name VARCHAR(255),
#                 state_url TEXT
#             )
#         """)

#         # CITIES TABLE
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS cities (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 state_name VARCHAR(255),
#                 city_name VARCHAR(255),
#                 city_url TEXT
#             )
#         """)
        
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)

#         # ---------------- STATE ----------------
#         if adapter.get("state") and adapter.get("state_url"):

#             self.cursor.execute("""
#                 INSERT INTO states (state_name, state_url)
#                 VALUES (%s, %s)
#             """, (
#                 adapter.get("state_name"),
#                 adapter.get("state_url")
#             ))

#         # ---------------- CITY ----------------
#         elif adapter.get("city") and adapter.get("city_url"):

#             self.cursor.execute("""
#                 INSERT INTO cities (state_name, city_name, city_url)
#                 VALUES (%s, %s, %s)
#             """, (
#                 adapter.get("state"),
#                 adapter.get("city"),
#                 adapter.get("city_url")
#             ))

#         self.conn.commit()
#         return item

#     def close_spider(self, spider):
#         self.cursor.close()
#         self.conn.close()

from itemadapter import ItemAdapter
import mysql.connector


class LawinfoPipeline:

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database="lawinfo_db"
        )
        self.cursor = self.conn.cursor()

        # STATES TABLE
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS states (
                id INT AUTO_INCREMENT PRIMARY KEY,
                state_name VARCHAR(255),
                state_url TEXT
            )
        """)

        # CITIES TABLE
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                id INT AUTO_INCREMENT PRIMARY KEY,
                state_name VARCHAR(255),
                city_name VARCHAR(255),
                city_url TEXT
            )
        """)

        # FIRMS TABLE ⭐ NEW
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS firms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city_name VARCHAR(255),
                firm_name VARCHAR(255),
                firm_url TEXT,
                firm_id VARCHAR(255)
            )
        """)
        # ---------------- FIRM DETAILS ⭐ NEW ----------------
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS firm_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                firm_name VARCHAR(255),
                job_title VARCHAR(255),
                phone VARCHAR(50),
                email VARCHAR(255),
                street_address TEXT,
                city VARCHAR(255),
                state VARCHAR(255),
                zipcode VARCHAR(20),
                firm_url TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attorney_details (
                id INT AUTO_INCREMENT PRIMARY KEY,

                atty_firm_name VARCHAR(255),
                atty_job_info TEXT,
                atty_phone VARCHAR(50),
                atty_email VARCHAR(255),

                atty_lawyer_name VARCHAR(255),
                atty_description TEXT,
                atty_lead_counsel_text TEXT,

                atty_practice_area VARCHAR(255),
                atty_verified_year VARCHAR(50),

                atty_street_address TEXT,
                atty_city VARCHAR(255),
                atty_state VARCHAR(255),
                atty_zipcode VARCHAR(20),

                atty_firm_url TEXT
            )
        """)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # ---------------- STATES ----------------
        if adapter.get("state_name") and adapter.get("state_url"):
            self.cursor.execute("""
                INSERT INTO states (state_name, state_url)
                VALUES (%s, %s)
            """, (
                adapter.get("state_name"),
                adapter.get("state_url")
            ))

        # ---------------- CITIES ----------------
        elif adapter.get("city_name") and adapter.get("city_url"):
            self.cursor.execute("""
                INSERT INTO cities (state_name, city_name, city_url)
                VALUES (%s, %s, %s)
            """, (
                adapter.get("state"),
                adapter.get("city_name"),
                adapter.get("city_url")
            ))

        # ---------------- FIRMS ⭐ NEW ----------------
        elif adapter.get("firm_name") and adapter.get("firm_url"):
            self.cursor.execute("""
                INSERT INTO firms (city_name, firm_name, firm_url, firm_id)
                VALUES (%s, %s, %s, %s)
            """, (
                adapter.get("city"),
                adapter.get("firm_name"),
                adapter.get("firm_url"),
                adapter.get("firm_id")
            ))
        # ---------------- FIRM DETAILS ⭐ NEW ----------------
        elif adapter.get("phone") or adapter.get("street_address") or adapter.get("zipcode"):

            self.cursor.execute("""
                INSERT INTO firm_details (
                    firm_name, job_title, phone, email,
                    street_address, city, state, zipcode, firm_url
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                adapter.get("firm_name"),
                adapter.get("job_info"),  
                adapter.get("phone"),
                adapter.get("email"),
                adapter.get("street_address"),
                adapter.get("city"),
                adapter.get("state"),
                adapter.get("zipcode"),
                adapter.get("url")
            ))

        elif adapter.get("atty_phone") or adapter.get("atty_street_address"):

            self.cursor.execute("""
                INSERT INTO attorney_details (
                    atty_firm_name,
                    atty_job_info,
                    atty_phone,
                    atty_email,
                    atty_lawyer_name,
                    atty_description,
                    atty_lead_counsel_text,
                    atty_practice_area,
                    atty_verified_year,
                    atty_street_address,
                    atty_city,
                    atty_state,
                    atty_zipcode,
                    atty_firm_url
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                adapter.get("atty_firm_name"),
                adapter.get("atty_job_info"),
                adapter.get("atty_phone"),
                adapter.get("atty_email"),
                adapter.get("atty_lawyer_name"),
                adapter.get("atty_description"),
                adapter.get("atty_lead_counsel_text"),
                adapter.get("atty_practice_area"),
                adapter.get("atty_verified_year"),
                adapter.get("atty_street_address"),
                adapter.get("atty_city"),
                adapter.get("atty_state"),
                adapter.get("atty_zipcode"),
                adapter.get("atty_firm_url")
            ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()