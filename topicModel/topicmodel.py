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
from gensim.test.utils import datapath

# spacy for lemmatization
import spacy
import en_core_web_sm

# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
import os
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

def read_json_file(path) -> []:
    with open(path) as f:
        return json.load(f)

def write_json_file(path, data):
    with open(path, 'w') as json_file:
        d = json.dumps(data)
        json_file.write(d)

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
def create_review_list(places) -> ():
    reviews = []
    placesReviewCounts = []
    for i, place in enumerate(places):
        placesReviewCounts.append(0)
        print('Processing: {}'.format(place['name']))
        for review in place['reviews']:
            r = process_review(review['text'])
            reviews.append(r)
            placesReviewCounts[i] += 1

    return reviews, placesReviewCounts

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
def create_lda_model(dictionary, corpus, num_topics):
    lda_model = gensim.models.LdaMulticore(corpus, num_topics=num_topics, id2word=dictionary,passes=50, workers=3)
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    return (lda_model, vis)

# Added the topics and distribution to the places and reviews within dataset
def add_dataset_topics(placesDataset, lda_model, corpus):
    review_count = 0
    placeCount = len(placesDataset) - 1
    for i, place in enumerate(placesDataset):
        print("Adding Topics: place {}/{}".format(i, placeCount))
        placeTopics = []
        for review in place['reviews']:
            reviewTopics = lda_model[corpus[review_count]]
            reviewTopics = sorted(reviewTopics, key=lambda x: (x[1]), reverse=True)
            review['topics'] = []
            for topic in reviewTopics:
                if topic[1] >= 0.2:
                    review['topics'].append({ "topic": topic[0], "dist": float(topic[1]) })
                    placeTopic = next((x for x in placeTopics if x["topic"] == topic[0]), None)
                    if placeTopic:
                        placeTopic["count"] += 1
                    else:
                        placeTopics.append({ "topic": topic[0], "count": 1 })
            review_count += 1
        placeTopics = sorted(placeTopics, key=lambda x: (x["count"]), reverse=True)
        place['review_topics'] = placeTopics

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

def write_topic_dist_file(lda_model, file_name, num_topics, num_words):
    topics = []
    topicsList = lda_model.print_topics(num_topics, num_words)
    for topic in topicsList:
        dist = []

        distStrings = str(topic[1]).split("+")
        for i, distString in enumerate(distStrings):
            if i == 0:
                dist.append({ 'term': distString[7:-2], "dist": float(distString[:5]) })
            else:
                dist.append({ 'term': distString[8:-2], "dist": float(distString[:6]) })  #0.047*\"bar\"
        topics.append({ 'topic': topic[0], "word_dist": dist })
    write_json_file(file_name, topics)

if __name__ == "__main__":
    num_topics = 40 
    num_words = 20
    model_path = "./model/model"

    # Parse all reviews from data set
    arr = os.listdir("../")
    path = '../dataset.json'
    print('Opening Dataset')
    placesDataset = read_json_file(path)
    
    reviews, placesReviewCounts = create_review_list(placesDataset)

    # Preform preprocessing on reviews
    processed_reviews = []
    review_count = len(reviews)
    for i, review in enumerate(reviews):
        print('processing {}/{}'.format(i, review_count))
        processed_reviews.append(preprocess(review)) 
    # write_lst(processed_reviews, './preprocessed_reviews.txt')
    # processed_reviews = read_lst('preprocessed_reviews.txt')

    print("Creating model")
    # dictionary that maps words and word IDs
    dictionary = gensim.corpora.Dictionary(processed_reviews)
    # Term Document Frequency
    corpus = [dictionary.doc2bow(review) for review in processed_reviews]
    lda_model, vis = create_lda_model(dictionary, corpus, num_topics)

    pyLDAvis.save_html(vis, "pyLDAvis.html")

    # Save model to disk.
    # file = datapath(model_path)
    # lda_model.save(model_path)
    
    # read model from disk
    # lda_model = gensim.models.LdaModel.load(model_path)

    write_topic_dist_file(lda_model, "topics.json", num_topics, num_words)

    add_dataset_topics(placesDataset, lda_model, corpus)
    write_json_file('newDS.json', placesDataset)
