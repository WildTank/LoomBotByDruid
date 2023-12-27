import scrapy


class LoomianSpider(scrapy.Spider):
    name = "loomians"
    start_urls = [
        "https://loomian-legacy.fandom.com/wiki/Loomian",
    ]

    def parse(self, response):
        for loomian in response.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr'):
            if (loomian.css("td:nth-child(1)::text").get() is not None):
                yield {
                    "id": loomian.css("td:nth-child(1)::text").get().strip(),
                    "name": loomian.css("a::text").get(),
                }

# scrapy runspider scraper.py -o loomians.json