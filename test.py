import sqlite3
import json
from scrapy.crawler import CrawlerProcess
import scraper
import time


connection = sqlite3.connect("loomianlegacy.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE loomians (id text, name text, action text)""")


# CHECKING EMPTY DATABASE FILE
print(">>>Checking Database File...")
time.sleep(2)
cursor.execute("""SELECT * FROM loomians""")
database = cursor.fetchall()
print(">>>Database Entries:")
for entry in database:
    print(entry[1])
print(">>>Database Should Be Empty!")
time.sleep(2)

# CHECKING EMPTY JSON FILE
try:
    print(">>>Checking JSON File...")
    time.sleep(2)
    file = open("loomians.json")
    data = json.load(file)
    print(">>>JSON File:")
    for i in data:
        print(i)
    print("\n")
    file.close()
    print(">>>JSON File Should Be Empty!")
    time.sleep(2)
except json.JSONDecodeError:
    print(">>>JSON File Is Empty!")

# SCRAPING AND WRITING TO JSON FILE
print(">>>Crawling Starting...")
time.sleep(2)
process = CrawlerProcess(
    settings = {
        "FEEDS": {
            "loomians.json": {"format": "json"}
        }
    }
)
process.crawl(scraper.LoomianSpider)
process.start()
print(">>>Crawling Finished!")
time.sleep(2)

# RECHECKING JSON FILE FOR THE SCRAPED DATA
print(">>>Rechecking JSON File...")
time.sleep(2)
file = open("loomians.json")
data = json.load(file)
print(">>>JSON File: ")
for i in data:
    print(i)
file.close()
print(">>>JSON File Should Have Data Now!")
time.sleep(2)

# WRITING SCRAPED DATA TO THE DATABASE
print(">>>Adding Scraped Data To Database")
time.sleep(2)
looms_tupArr = []
for i in data:
    looms_tupArr.append((i['id'], i['name'], "Esc"))
cursor.executemany("""INSERT INTO loomians VALUES (?, ?, ?)""", looms_tupArr)

# RECHECKING DATABASE FILE FOR LOOMIAN ENTRIES
print(">>>Rechecking Database File...")
time.sleep(2)
cursor.execute("""SELECT * FROM loomians""")
database = cursor.fetchall()
print(">>>Database Entries:")
for entry in database:
    print(entry)
print(">>>Database Should Have Entries Now!")
time.sleep(2)


open("loomians.json", "w").close()  # clears loomian JSON file
cursor.execute("""DELETE FROM loomians""")
cursor.execute("""DROP TABLE loomians""")
connection.commit()
connection.close()
