from flask import Flask
from flask import Flask, request, render_template
from kaggle.api.kaggle_api_extended import KaggleApi

app = Flask(__name__)

def check_file_type(files):
    image = 0
    csv = 0
    if files.files[0].fileType.lower() in ['.jpg', '.png', '.webp','.tif']:
        image += 1
    elif files.files[0].fileType.lower() in ['.csv' ]:
        csv += 1
    print(image, csv)


'''api = KaggleApi()
api.authenticate()
text = 'google'
datasets = api.dataset_list(search=text)
for dat in datasets:
    check_file_type(api.dataset_list_files(dat.ref))


api = KaggleApi()
api.authenticate()
text = 'Google'
print(text)
datasets = api.dataset_list(search=text)
for dat in datasets:
    check_file_type(api.dataset_list_files(dat.ref))api_secret = '924eeda9ef2b4b5d9d41013ffdb7cd30'


import requests
import urllib
import json
import pprint

# Make the HTTP request.
response = requests.get('http://catalog.data.gov/api/3/action/package_search?q='+'camp&rows=50')
assert response.status_code == 200

# Use the json module to load CKAN's response into a dictionary.
response_dict = json.loads(response.content)

# Check the contents of the response.
assert response_dict['success'] is True
result = response_dict['result']
dataset=[]
for res in response_dict['result']['results']:
    tags = []
    for tag in res['tags']:
        tags.append(tag['name'])
    try:
        contentUrl = res['resources'][0]['url']
    except:
        contentUrl = 'empty'
    dataset.append({'name': res['title'],
                    'source': "Data.Gov",
                    'size': None,
                    'alternateName': res['notes'],
                    'url': 'https://catalog.data.gov/dataset/' + res['name'],
                    'tags': tags,
                    'contentUrl': contentUrl})


apiSecret = '924eeda9ef2b4b5d9d41013ffdb7cd30'
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key=apiSecret)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
text = 'camp'
response = requests.get('http://catalog.data.gov/api/3/action/package_search?q=' +text+ '&rows=50')
response_dict = json.loads(response.content)'''

from sodapy import Socrata

client = Socrata("data.kcmo.org", None)

client.datasets()