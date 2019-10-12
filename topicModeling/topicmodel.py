import re
import numpy as np
import pandas as pd
import json
from pprint import pprint

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Gensim
import gensim
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy
import en_core_web_sm

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
"""
documentation

# Run in python console
import nltk; nltk.download('stopwords')

pip install numpy
pip install -U gensim
pip install pyLDAvis

// gets spacy model
python -m spacy download en
"""

def getJsonData(path) -> []:
    with open(path) as f:
        return json.load(f)

def write_lst(lst,file_):
    with open(file_,'w') as f:
        for l in lst:
            f.write(" ".join(l))
            f.write('\n')

def read_lst(file):
    # lines = [[]]
    return [line.rstrip('\n').split() for line in open(file)]

# remove random charaters
def process_review(review):
    review = review.encode('ascii',errors='ignore').decode('utf-8') #removes non-ascii characters
    review = re.sub('\s+',' ',review)   #replaces repeated whitespace characters with single space
    review = re.sub("\'", "", review)   #Remove distracting single quotes
    return review

# Create list of reviews from dataset
def create_reviewlist(path) -> []:
    print('Opening Dataset')
    places = getJsonData(path)

    reviews = []
    for place in places:
        print('Processing: {}'.format(place['name']))
        for review in place['reviews']:
            r = process_review(review['text'])
            reviews.append(r)

    return reviews

# Preforms lemmatization and stemming of passed in tokens
def lematize_stem(tokens):
    pos_filter = ['NOUN', 'ADJ', 'VERB', 'ADV']
    stemmer = PorterStemmer()
    nlp = en_core_web_sm.load()
    doc = nlp(" ".join(tokens)) 
    lemma_words = [stemmer.stem(token.lemma_) for token in doc if token.pos_ in pos_filter]
    return lemma_words

# Preforms preprocessing of review list
def preprocess(review):
    tokens = []
    stop_words = stopwords.words('english')
    for token in gensim.utils.simple_preprocess(review):
        if token not in stop_words and len(token) > 2:
            tokens.append(token)
    processed_review = lematize_stem(tokens)
    return processed_review

# Creates LDA Model
def create_lda_model(processed_reviews):
    # dictionary that maps words and word IDs
    dictionary = gensim.corpora.Dictionary(processed_reviews)

    # Term Document Frequency
    corpus = [dictionary.doc2bow(review) for review in processed_reviews]

    # tfidf = gensim.models.TfidfModel(corpus)
    # corpus_tfidf = tfidf[corpus]

    lda_model = gensim.models.LdaMulticore(corpus, num_topics=40, id2word=dictionary,passes=50, workers=3)
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    return (lda_model, vis)

# Computes coherence value of varying topic numbers
def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    coherence_values = []
    model_list = []

    for num_topics in range(start, limit, step):
        print('Generating model with {} topics'.format(num_topics))
        model = gensim.models.LdaMulticore(corpus, num_topics=num_topics, id2word=dictionary,passes=50, workers=3)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values

if __name__ == "__main__":
    # Parse all reviews from data set
    path = '../dataset.json'
    reviews = create_reviewlist(path)

    # Preform preprocessing on reviews
    processed_reviews = []
    review_count = len(reviews)
    for i, review in enumerate(reviews):
        print('processing {}/{}'.format(i, review_count))
        processed_reviews.append(preprocess(review)) 
    # write_lst(processed_reviews, './processed_reviews.txt')
    # processed_reviews = read_lst('processed_reviews.txt')

    print("Creating model")
    lda_model, vis = create_lda_model(processed_reviews)

    pprint(lda_model.print_topics(num_topics=40, num_words=10))
    pyLDAvis.save_html(vis, "pyLDAvis.html")
