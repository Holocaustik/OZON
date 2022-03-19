import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# from scrapy.item import Item, Field
# from ozon.items import Product



class ParserOzonSpider(scrapy.Spider):
    name = 'parser_ozon'
    allowed_domains = ['ozon.ru/brand/stavr']
    start_urls = ['https://www.ozon.ru/brand/stavr-26303509/']

    def parse(self, response):
        for link in response.css('div.h4y hy5 a::attr(href)'):
            yield response.follow(link, callback=self.parse_card)

    def parse_card(self, response):
        yield {
            'name': response.css('h1.kp4').get(),
            'price': response.css('span.o1k').get(),
            'raite': response.css('div.ui-ab8').get(),
        }

