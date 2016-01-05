import os
from os import path
root = "/Users/.../.../topicmodel_speeches"
files = os.listdir(root)

#load speeches into a list
docs = list() 
for file in files:
    with open(path.join(root, file), 'r') as fd:
       txt = fd.read()
       docs.append(txt)

# clean speeches
import re 
def clean(doc):
    doc = re.sub(r'[^\w\s]*', '', doc) 
    doc = re.sub(r'[\s]+', ' ', doc)
    doc = doc.lower().strip()
    return doc

clean_docs = list()
for doc in docs:
    doc = clean(doc)
    clean_docs.append(doc)

#tokenize speeches
token_docs = list()
for doc in clean_docs:
    token_docs.append(doc.split())

#remove stopwords
stopwords = list()
with open('/Users/.../.../topicmodel_stopwords.txt', 'r') as fd:
    for line in fd.readlines():
        stopwords.append(line.strip())

sw_token_docs = list()
for doc in token_docs:
    sw_doc = list()
    for token in doc:
        if not token in stopwords:
            sw_doc.append(token)
    sw_token_docs.append(sw_doc)

# perform topic modelling
from gensim import corpora, models, similarities
dictionary = corpora.Dictionary(sw_token_docs)
corpus = [dictionary.doc2bow(doc) for doc in sw_token_docs]

import logging, gensim
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
lda = gensim.models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=25, update_every=1, passes=20)

#print 25 topics out to 20 words
t=0
for i in lda.show_topics(num_topics=25, num_words=20, log=False, formatted=True):
    print "Topic # ", t , i
    t = t + 1

#print topic weight in each speech    
count=1
for doc in sw_token_docs:
    vec = dictionary.doc2bow(doc)
    print "Speech # ", count, lda[vec]
    #print first 100 words of speech to verify correct speech
    print doc[0:100]
    count = count + 1

