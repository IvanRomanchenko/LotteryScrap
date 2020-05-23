# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timezone, timedelta
import pytz 


class OregonLotterySpider(scrapy.Spider):
    name = "oregon_lottery"
    start_urls = ["https://www.oregonlottery.org/games/draw-games/keno/past-results/"]
        
    def parse(self, response):
        for i in response.xpath("//table[contains(@class, 'responsive keno-table')]/tr")[1:]:
            yield {
                "externalId": f"oregonKeno_{i.xpath('.//td[2]/text()').get()}",
                "drawDate": pytz.timezone("America/Los_Angeles").localize(datetime.strptime(i.xpath('.//td[1]/text()').get(), '%m/%d/%Y %H:%M%p')).astimezone(tz=timezone.utc).isoformat(),
                "numbers": [int(j) for j in i.xpath('.//td/text()')[2:22].getall()],
                "created": datetime.utcnow().isoformat(timespec='seconds') + '+00:00'
                }
            