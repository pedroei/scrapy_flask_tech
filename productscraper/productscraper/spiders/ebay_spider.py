import scrapy
from ..items import ProductscraperItem
from datetime import datetime


class EbaySpider(scrapy.Spider):
    name = 'ebay'
    count = 0
    term = ''
    
    def __init__(self, *args, **kwargs): 
        super(EbaySpider, self).__init__(*args, **kwargs)

        self.term = kwargs.get('term')
        self.start_urls = ['https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={}&_sacat=0'.format(kwargs.get('term'))]

    def parse(self, response):
        for products in response.css('.s-item'):
            self.count+=1
            prod_name = products.css('.s-item__title::text').get()
            prod_price = products.css('span.s-item__price::text').get()
            prod_price_hundred = -1
            prod_img = products.css('img.s-item__image-img').xpath('@src').get()
            prod_link = products.css('a.s-item__link').xpath('@href').get()
            scrape_date_time = datetime.now()
            scrape_date = datetime.today().strftime('%Y-%m-%d')

            if prod_price is None:
                prod_price = 'Not specified'
            else:
                prod_price = prod_price.replace('EUR ','')

            if prod_price != 'Not specified':
                prod_price_hundred = round(float(prod_price.replace(',', '.')), -2)

            if self.term == 'favicon.ico':
                self.term = 'none'

            if prod_name is None:
                self.count-=1
                yield 
            else: 
                yield {
                    'id': self.count,
                    'name': prod_name,
                    'price': prod_price,
                    'price_hundred': prod_price_hundred,
                    'image': prod_img,
                    'link': prod_link,
                    'store': 'Ebay',
                    'scrape_date_time': scrape_date_time,
                    'scrape_date': scrape_date,
                    'term': self.term
                }
        #TODO: next page
