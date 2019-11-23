from flask import Flask, redirect, url_for, request,render_template
import nltk

import re
import bs4 as bs
import urllib.request
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('treebank')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

@app.route('/login',methods = ['POST', 'GET'])
def login():
    user = request.form['nm']
    a=str(user)
    scraped_data= urllib.request.urlopen(a)
    article = scraped_data.read()
    parsed_article = bs.BeautifulSoup(article,'html')
    paragraphs = parsed_article.find_all('p')
    text= ""
    for p in paragraphs:
   	    text += p.text
    text= re.sub(r'\[[0-9]*\]', ' ',text)
    text = re.sub(r'\s+', ' ',text)
    format_text = re.sub('[^a-zA-Z]', ' ', text )
    format_text = re.sub(r'\s+', ' ', format_text)
    from nltk.tokenize import sent_tokenize
    sentence=[]
    for i in sent_tokenize(text):
        sentence.append(i)
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    from nltk.tokenize import word_tokenize
    d= {}
    a=word_tokenize(format_text)
    a
    for word in a:
        if word not in stop_words:
            if word not in d:
                d[word.lower()] = 1
            else:
                d[word.lower()] += 1
    maxf=max(d.values())
    for word in d:
        d[word] = (d[word]/maxf)
    sentence_scores= {}
    for sent in sentence:
            for word in nltk.word_tokenize(sent.lower()):
                if word in d.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = d[word]
                        else:
                            sentence_scores[sent] += d[word]
    c=0
    sentence_scores_updated=sorted(sentence_scores.items(), reverse=True, key=lambda t: t[1])
    sentence_scores_updated
    s=""
    for i,j in sentence_scores_updated:
        if c<=3:
            s=s+str(i)
        c=c+1

    return s

if __name__ == '__main__':
   app.run(debug = True)
