import scrapy
from datetime import datetime, timezone, timedelta
import pytz 

from scrapy.http import FormRequest


class OregonLotterySpider(scrapy.Spider):
    name = "oregon_lottery"
    start_urls = ["https://www.oregonlottery.org/games/draw-games/keno/past-results/"]

    def parse(self, response):
        return FormRequest.from_response(response, formxpath="//a[contains(@class, 'pagination-show-all')]", formdata={
            'ctl22_TSSM': ';Telerik.Sitefinity.Resources, Version=10.2.6602.0, Culture=neutral, PublicKeyToken=b28c218413bdf563:en:1c3e6627-a90c-4375-b55c-75906376ec60:7a90d6a',
            '__VIEWSTATE': '/wEPDwUKLTY1MzU2OTUwMmRkvA+XEUVx78gBN+PYgqp1AOoTZU2JKdB4oRoX9Q5fBVo=',
            '__VIEWSTATEGENERATOR': '81854762',
            'PageSize': '0'
        }, method='POST', callback=self.after_parse)

    def after_parse(self, response):
        for i in response.xpath("//table[contains(@class, 'responsive keno-table')]/tr")[1:]:
            yield {
                "externalId": f"oregonKeno_{i.xpath('.//td[2]/text()').get()}",
                "drawDate": pytz.timezone("America/Los_Angeles").localize(datetime.strptime(i.xpath('.//td[1]/text()').get(), '%m/%d/%Y %H:%M%p')).astimezone(tz=timezone.utc).isoformat(),
                "numbers": [int(j) for j in i.xpath('.//td/text()')[2:22].getall()],
                "created": datetime.utcnow().isoformat(timespec='seconds') + '+00:00'
                }
            