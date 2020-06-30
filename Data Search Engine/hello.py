from os.path import sep
from sodapy import Socrata
from flask import Flask, render_template, request, make_response
import json
from kaggle.api.kaggle_api_extended import KaggleApi
from newsapi import NewsApiClient
import requests
import random
import json

count = 0
datasetCount = 1
oldTerm = ''
newsPage = 1
client = Socrata("data.kcmo.org", None)

app = Flask(__name__, template_folder='templates')

def check_file_type(files):
    image = 0
    csv = 0
    if files.files[0].fileType.lower() in ['.jpg', '.png', '.webp','.tif']:
        return 'Image'
    elif files.files[0].fileType.lower() in ['.csv' ]:
        return 'CSV'
    elif files.files[0].fileType.lower() in ['.json' ]:
        return 'JSON'
    elif files.files[0].fileType.lower() in ['.xml' ]:
        return 'XML'
    elif files.files[0].fileType.lower() in ['.ndjson' ]:
        return 'NdJSON'

@app.route('/')
def my_form():
    #return "Hello World"
    return render_template('data.html')

@app.route('/', methods=['POST'])
def my_form_post():
    api = KaggleApi()
    print('Hello')
    api.authenticate()
    text = request.form['text']
    datasets = api.dataset_list(search=text)
    response = requests.get('http://catalog.data.gov/api/3/action/package_search?q=' +text+ '&rows=50')
    response_dict = json.loads(response.content)
    dataset = list()
    for dat in datasets:
        dataset.append({'name':dat.title,
            'source':'Kaggle',
            'size':dat.size,
            'alternateName':dat.subtitle,
            'url':dat.url,
            'tags':dat.tags,
            'contentUrl':'https://www.kaggle.com/'+dat.ref+'/download'})

    for res in response_dict['result']['results']:
        tags = []
        for tag in res['tags']:
            tags.append(tag['name'])
        try:
            contentUrl=res['resources'][0]['url']
        except:
            contentUrl='empty'
        dataset.append({'name':res['title'],
        'source':"Data.Gov",
        'size':None,
        'alternateName':res['notes'],
        'url':'https://catalog.data.gov/dataset/' + res['name'],
        'tags':tags,
        'contentUrl':contentUrl})


    random.shuffle(dataset)
    return  render_template('data.html', datasetInfo=dataset, value=text)

@app.route('/loaddata')
def loaddata():
    print("ImHere")
    source = request.args.get('source')
    term = request.args.get('term')
    global oldTerm, count, datasetCount, newsPage
    if(term != oldTerm):
        oldTerm = term
        print("this ran")
        count = 0
        datasetCount = 1
        newsPage = 1
    if(source=='Kaggle'):
        api = KaggleApi()
        api.authenticate()
        text = term
        print(text)
        datasets = api.dataset_list(search=text, page = datasetCount)
        if not datasets:
            print("here")
        dataset = []
        i=0
        for dat in datasets[count:count+4]:
            i = i+1
            print(dat)
            dataset.append({'name': dat.title,
                            'source': 'Kaggle',
                            'size': dat.size,
                            'alternateName': dat.subtitle,
                            'url': dat.url,
                            'date': str(dat.lastUpdated),
                            'tags': str(dat.tags),
                            'contentUrl': 'https://www.kaggle.com/' + dat.ref + '/download',
                            'fileType': check_file_type(api.dataset_list_files(dat.ref))})
        count = count + len(dataset)
        if not dataset:
            datasetCount += 1
            print(datasetCount)
            count = 0
        resu = make_response(json.dumps(dataset), 200)
        return resu
    elif(source=='News'):
        print(newsPage)
        apiSecret = '924eeda9ef2b4b5d9d41013ffdb7cd30'
        newsapi = NewsApiClient(api_key=apiSecret)
        all_articles = newsapi.get_everything(q=term,
                                              language='en',
                                              sort_by='relevancy',
                                              page=newsPage)
        newsPage += 1
        resu = make_response(json.dumps(all_articles['articles']), 200)
        return resu
    elif(source=='Data.gov'):
        print('Data.Gov')
        response = requests.get('http://catalog.data.gov/api/3/action/package_search?q=' +term+ '&rows=50')
        response_dict = json.loads(response.content)
        resu = make_response(json.dumps(response_dict['result']['results']), 200)
        return resu
    elif(source=='KCMO.org'):
        global client
        print('KCMO.org')
        result = client.datasets(q=term)
        resu = make_response(json.dumps(result), 200)
        return resu



if __name__ == '__main__':
    app.run()
