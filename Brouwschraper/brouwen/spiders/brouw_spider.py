from scrapy import Spider
from scrapy.http.request import Request
from scrapy.selector import Selector
from brouwen.items import BrouwItem

class brouwspider(Spider):
    name = "mout_details"
    allowed_domains = ["braumarkt.com"]
    start_urls = ["https://www.braumarkt.com/onze-producten/bierbrouwen/mout-granen/the-swaen-kloosterzande/basic-swaen.html"]

    def parse(self, response):
        for url in response.xpath('//h2[@class="product-name"]/a'):
            yield response.follow(url, callback=self.parse_details)

    def parse_details(self, response):
        prod_details = response.xpath('//div[@class="std"]/ul//li/text()').extract()
       
        d1 = {k[0]:k[1].strip() for k in [x.split(":") for x in prod_details]}
       
        d1['Name'] = response.xpath('//h1[@itemprop="name"]/text()').extract()[0]
       
        #checken op aanbieding en prijs opslaan
        if response.xpath('.//p[@class="special-price"]'):
            prijs = response.xpath('.//p[@class="special-price"]/span/text()').extract()[0].strip()
        else:
            prijs = response.xpath('.//span[@class="price"]/text()').extract()[0].strip()
        
        d1['Price'] = prijs

        yield d1