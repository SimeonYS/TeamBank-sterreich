import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from ..items import TeambankItem
import re
pattern = r'(\r)?(\n)?(\t)?(\xa0)?'

class TeamSpider(scrapy.Spider):
    name = 'team'

    start_urls = ['http://www.teambank.at/medien/presse/#/']

    def parse(self, response):
        rows = response.xpath('//li[@class="release"]')
        for row in rows:
            date = row.xpath('.//h3/text()').get()
            link = row.xpath('.//a/@href').get()
            yield response.follow(link, self.parse_article, cb_kwargs=dict(date=date))

    def parse_article(self, response, date):
        item = ItemLoader(TeambankItem())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//div[@class="content"]//h2/text()').get()
        content = ''.join(response.xpath('//div[@class="module paragraph regular"]//text()').getall())
        content = re.sub(pattern, "", content)

        item.add_value('date', date)
        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        return item.load_item()
