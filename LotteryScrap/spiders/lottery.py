from datetime import datetime
import scrapy


class LotterySpider(scrapy.Spider):
    name = 'lottery'
    start_urls = ["https://igra.msl.ua/megalote/ru/archive/"]

    def parse(self, response):
        for i in response.xpath("//div[contains(@class, 'archive_results-item')]"):
            yield {
                "edition": i.xpath(".//a[contains(@class, 'archive_result-number')]/text()").re(r"\d+")[0],
                "result-year": i.xpath(".//p[contains(@class, 'archive_result-date')]/text()").re(r"\d{4}")[0],
                "created-time": datetime.utcnow().isoformat(timespec='seconds') + '+00:00',
                "numbers": [int(j) for j in i.xpath(".//span[contains(@class, 'ball-number')]/text()").getall()]
            }

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)
        
