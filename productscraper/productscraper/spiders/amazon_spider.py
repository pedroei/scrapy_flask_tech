import scrapy
import re
from datetime import datetime


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    count = 0
    term = ''

    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)

        self.term = kwargs.get('term')
        self.start_urls = ['https://www.amazon.es/s?k={}'.format(self.term)]

    def parse(self, response):
        for products in response.css('div.sg-col-inner'):
            self.count += 1
            prod_name = products.css('.a-size-base-plus.a-color-base.a-text-normal::text').get()
            prod_price = products.css('.a-price-whole::text').get()
            prod_price_hundred = -1
            prod_img = products.css('img.s-image').xpath('@src').get()
            prod_link = products.css('.a-link-normal.a-text-normal').xpath('@href').get()
            scrape_date_time = datetime.now()
            scrape_date = datetime.today().strftime('%Y-%m-%d')

            if prod_price is None:
                prod_price = 'Not specified'

            if prod_price != 'Not specified' and ',' in prod_price:
                prod_price = re.sub('\s+', '', prod_price)
                prod_price = prod_price.replace(',', '.')
                if prod_price.count('.'):
                    prod_price = prod_price.replace('.', '', 1)
                prod_price_hundred = round(float(prod_price), -2)

            if prod_link is not None:
                prod_link = 'https://www.amazon.es' + prod_link

            if self.term == 'favicon.ico':
                self.term = 'none'

            if prod_name is None:
                self.count -= 1
                yield
            else:
                yield {
                    'id': self.count,
                    'name': prod_name,
                    'price': prod_price,
                    'price_hundred': prod_price_hundred,
                    'image': prod_img,
                    'link': prod_link,
                    'store': 'Amazon ES',
                    'scrape_date_time': scrape_date_time,
                    'scrape_date': scrape_date,
                    'term': self.term
                }

        next_page = response.css('li.a-last>a').xpath('@href').get()
        print('https://www.amazon.es/' + next_page)
        if next_page is not None:
            yield scrapy.Request('https://www.amazon.es/' + next_page, callback=self.parse, dont_filter=True)

# command:  scrapy crawl amazon -a term="pc" -O products.json
