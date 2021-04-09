import scrapy
from ..items import ProductscraperItem
from datetime import datetime

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    count = 0
    
    def __init__(self, *args, **kwargs): 
        super(AmazonSpider, self).__init__(*args, **kwargs) 

        self.start_urls = ['https://www.amazon.es/s?k={}&ref=nb_sb_noss_2'.format(kwargs.get('term'))]

    def parse(self, response):
        for products in response.css('div.sg-col-inner'):
            self.count+=1
            prod_name = products.css('.a-size-base-plus.a-color-base.a-text-normal::text').get()
            prod_price = products.css('.a-price-whole::text').get()
            prod_img = products.css('img.s-image').xpath('@src').get()
            prod_link = products.css('.a-link-normal.a-text-normal').xpath('@href').get()
            scrape_date = datetime.now()

            if prod_price is None:
                prod_price = 'Not specified'

            if prod_link is not None:
                prod_link = 'https://www.amazon.es' + prod_link

            if prod_name is None:
                self.count-=1
                yield 
            else: 
                yield {
                    'id': self.count,
                    'name': prod_name,
                    'price': prod_price,
                    'image': prod_img,
                    'link': prod_link,
                    'store': 'Amazon ES',
                    'scrape_date': scrape_date
                }
        #TODO: next page
        #next_page = response.css('li.a-last>a').attrib['href']
        #if next_page is not None:
        #    yield response.follow('https://www.amazon.es/-/pt/s?k=pc&page=2', callback=self.parse)

# command:  scrapy crawl amazon -a term="pc" -O products.json