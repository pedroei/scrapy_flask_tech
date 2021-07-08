import scrapy
import re
from datetime import datetime


class KuantoKustaSpider(scrapy.Spider):
    name = 'kuantokusta'
    count = 0
    term = ''

    def __init__(self, *args, **kwargs): 
        super(KuantoKustaSpider, self).__init__(*args, **kwargs)

        self.term = kwargs.get('term')
        print(self.term)
        self.start_urls = ['https://www.kuantokusta.pt/search?q={}'.format(kwargs.get('term'))]

    def parse(self, response):
        for products in response.css('.product-item-wrapper'):
            self.count+=1
            prod_name = products.css('.product-item-name::attr(title)').get()
            prod_price = products.css('span.big-price-interval::text').get()
            prod_price_hundred = -1
            prod_img = products.css('.img-responsive').xpath('@src').get()
            prod_link = 'https://www.kuantokusta.pt' + products.css('.btn.product-item-btn').attrib['href']
            scrape_date_time = datetime.now()
            scrape_date = datetime.today().strftime('%Y-%m-%d')

            if prod_price is None:
                prod_price = 'Not specified'
            else:
                prod_price = prod_price.split("\u20ac", 1)[0]

            if prod_price != 'Not specified' and ',' in prod_price:
                prod_price = re.sub('\s+', '', prod_price)
                prod_price = prod_price.replace(',', '.')
                prod_price_hundred = round(float(prod_price), -2)

            if prod_img == '/responsive/imgs/kk-lazing-loading.gif':
                prod_img = products.css('.img-responsive').xpath('@onerror').get().replace("this.src = '", "").replace("'", "")

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
                    'store': 'KuantoKusta',
                    'scrape_date_time': scrape_date_time,
                    'scrape_date': scrape_date,
                    'term': self.term
                }

        next_page = response.css('li.ais-pagination--item.pagination-item.ais-pagination--item__next>a.ais-pagination--link').xpath('@href').get()
        print(next_page)
        if next_page is not None:
            print('entered')
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
