import scrapy
from ..items import ProductscraperItem
from datetime import datetime

class KuantoKustaSpider(scrapy.Spider):
    name = 'kuantokusta'
    count = 0

    def __init__(self, *args, **kwargs): 
        super(KuantoKustaSpider, self).__init__(*args, **kwargs) 

        self.start_urls = ['https://www.kuantokusta.pt/search?q={}'.format(kwargs.get('term'))]

    def parse(self, response):
        for products in response.css('.product-item-wrapper'):
            self.count+=1
            prod_name = products.css('.product-item-name::attr(title)').get()
            prod_price = products.css('span.big-price-interval::text').get()
            prod_img = products.css('.img-responsive').xpath('@src').get()
            prod_link = 'https://www.kuantokusta.pt' + products.css('.btn.product-item-btn').attrib['href']
            scrape_date = datetime.now()

            if prod_price is None:
                prod_price = 'Not specified'
            else:
                prod_price = prod_price.split("\u20ac", 1)[0]

            if prod_img == '/responsive/imgs/kk-lazing-loading.gif':
                prod_img = products.css('.img-responsive').xpath('@onerror').get().replace("this.src = '", "").replace("'", "")

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
                    'store': 'KuantoKusta',
                    'scrape_date': scrape_date
                }
        #TODO: next page


        #items = ProductscraperItem()

        #product_name = response.css('.product-item-name::attr(title)').extract()
        #product_price = response.css('.big-price-interval::text').extract()
        
        #items['product_name'] = product_name
        #items['product_price'] = product_price

        #yield items
