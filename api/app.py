from __future__ import unicode_literals
import json
import requests
import pandas as pd

from flask import Flask, request, Response, render_template, session, redirect, url_for, jsonify

websites_to_scrape = ['amazon', 'ebay', 'kuantokusta']

def scrape_website(website_name, term):
    params = {
        'spider_name': website_name,
        'start_requests': True,
        'term': term
    }
    response = requests.get('http://localhost:3000/crawl.json', params)
    data = json.loads(response.text)
    items = data['items']

    items_name = website_name + "_items"
    res = {
        items_name: items
    }
    return res

app = Flask(__name__)

@app.route('/<term>')
def scrape(term):
    response = {}

    for website in websites_to_scrape:
        website_data = scrape_website(website, term)
        response.update(website_data)

    return response

@app.route('/lowest/<term>')
def scrapeLowest(term):
    data = []

    for website in websites_to_scrape:
        website_data = scrape_website(website, term)
        data = data + website_data[website + "_items"]

    elem_count = 0
    for element in data:
        elem_count += 1
        
        del element["id"]
        element["id"] = elem_count

        if element["price"] != "Not specified":
            element["price"] = element["price"].replace(".", "").replace('\xa0', '')
            element["price"] = float(element["price"].replace(",", "."))
        else:
            element["price"] = 0

    #TODO: replace the ones with price=0 to "Not specified" & put them on the end
    sortedList = sorted(data, key=lambda x: x['price'])

    return jsonify(sortedList)
       
if __name__ == '__main__':
    app.run(debug=True, port=1234)

#source venv/bin/activate
#scrapyrt -p 3000 --> para começar a "api" do scrapy