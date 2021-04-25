from __future__ import unicode_literals
import json, bson
import requests
import pandas as pd
import pymongo
from bson import ObjectId

from flask import Flask, request, Response, render_template, session, redirect, url_for, jsonify
from pymongo import MongoClient

cluster = MongoClient('localhost', 27017)
db = cluster["products"]
collection = db['products']

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

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

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

    sortedList = sorted(data, key=lambda x: x['price'])

    for sortedElement in sortedList:
        if sortedElement["price"] == 0:
            sortedElement["price"] = "Not specified"

    newSortedList = sorted(sortedList, key=lambda x: x['price'] == 'Not specified')

    return jsonify(newSortedList)

@app.route('/previous')
def getPreviousData():
    results = []

    # for product in collection.find({"name": "/.*" + name + ".*/"}):
    for product in collection.find():
        product['_id'] = str(product['_id'])
        product["scrape_date"] = product["scrape_date"].strftime("%m/%d/%Y, %H:%M:%S")
        results.append(product)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=1234)

#source venv/bin/activate
#scrapyrt -p 3000 --> para começar a "api" do scrapy