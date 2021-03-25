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

@app.route('/')
def scrape():
    response = {}

    for website in websites_to_scrape:
        website_data = scrape_website(website, "laptop")
        response.update(website_data)

    return response
       
if __name__ == '__main__':
    app.run(debug=True, port=1234)