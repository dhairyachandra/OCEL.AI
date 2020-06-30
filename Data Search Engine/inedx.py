from os.path import sep

from flask import Flask, request, render_template
from nltk.corpus import wordnet as wn
import json
import csv
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__, template_folder='templates')

@app.route('/')
def my_form():
    # return "Hello World"
    return render_template('searchForm.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    #fi = open('static/js/wordcloud.csv', 'w')
    lis = list()
    for query in text.split(' '):
        for ss in wn.synsets(query):
            for l in ss.lemmas():
                if l.name() not in lis:
                    lis.append({'text' : l.name()})

    print(json.dumps(lis))
    '''print(os.getcwd())
    with open('static/js/wordcloud.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in lis:
            spamwriter.writerow(x)'''
    #fi.write('words\n')
    #for x in lis:
    #    fi.write(x)
    #    fi.write('\n')
    #fi.close()
    return render_template('index2.html', data = lis)


if __name__ == '__main__':
    app.run()
