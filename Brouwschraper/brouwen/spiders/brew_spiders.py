from scrapy import Spider
from scrapy.selector import Selector
from brouwen.items import BrouwItem
import unicodedata
import re

re_weight = re.compile(r"\d+\sKG", re.I)
re_merk = re.compile(r"(.*)\s\d", re.I)


brands = {'swaen': 'Swaen',
         'dingemans': 'Dingemans',
         'weyermann': 'Weyermann',
         'thomas fawcett': 'Thomas Fawcett',
         'castle':'Castle Malting'}


def findbrand(tekst):
    for k in brands:
        if k in tekst.lower():
            return brands.get(k)

class BrouwmarktSpider(Spider):
    name = "mout"
    allowed_domains = ["braumarkt.com/"]
    start_urls = ["https://www.braumarkt.com/onze-producten/bierbrouwen/mout-granen/the-swaen-kloosterzande.html?limit=144"]
    
    def parse(self, response):
        #kenmerken = Selector(response).css(".bottom-bar-product-list")
        kenmerken = Selector(response).xpath('//div[@class="bottom-bar-product-list"]')

        for kenmerk in kenmerken:
            item = BrouwItem()
            
            #productbeschrijving opslaan als prod_text
            prod_text = kenmerk.xpath('.//h2[@class="product-name"]/a/text()').extract()[0]
            merk = re.search(re_merk, prod_text).group(1)
            item['merk'] = merk.replace('© ', '')

            #gewicht
            item['gewicht'] = re.search(re_weight, prod_text).group()
            
            #checken op aanbieding en prijs opslaan
            if kenmerk.xpath('.//p[@class="special-price"]'):
                prijs = kenmerk.xpath('.//p[@class="special-price"]/span/text()').extract()[0].strip()
            else:
                prijs = kenmerk.xpath('.//span[@class="price"]/text()').extract()[0].strip()
            item['prijs'] = prijs
            
            
            yield item




            