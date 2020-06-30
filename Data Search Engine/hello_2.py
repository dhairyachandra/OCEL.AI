from os.path import sep

from flask import Flask, request, render_template
from kaggle.api.kaggle_api_extended import KaggleApi
import requests
from bs4 import BeautifulSoup
import json


app = Flask(__name__)

@app.route('/')
def my_form():
    #return "Hello World"
    return render_template('searchForm.html')

@app.route('/', methods=['POST'])
def my_form_post():
    api = KaggleApi()
    api.authenticate()
    text = request.form['text']
    datasets = api.dataset_list(search=text)
    datasetInfo= list()
    for dat in datasets:
        y = BeautifulSoup(requests.get('https://www.kaggle.com/'+dat.ref).content, 'html.parser')
        z = json.loads(str(y.find('script', type="application/ld+json").string))
        datasetInfo.append(z)

    print(datasetInfo)

    for dat, data in zip(datasets, datasetInfo):
        print(dat)


    return  render_template('data.html', datasets=datasets, datasetInfo=datasetInfo)

if __name__ == '__main__':
    app.run()
