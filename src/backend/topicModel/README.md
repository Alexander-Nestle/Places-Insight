# File Descriptions

### Model Directory
Contains the generated topic model.  Gensim library can readin these files to produce a lda_model object.  

Code to do this can be found in TopicModelGenerator.py.

#### preprocessd_reviews.txt
Contains preprocessed reviews for LDA model (linting, stemming, etc)

## pyLDAvis.html
HTML file that allows for a detailed visualization for the topics.  

NOTE: topic numbers in visualization do not correlate with topics from model/json file.

## TopicModelGenerator.py
All the code needed for generating topic model using LDA.

## TopicModelService.py
Contains code to utilize topic model.

## topics.json
Contains all topics and the word distributions.

## JsonIO.py
All Json IO code used by topic model modules.

## topicInvertedIndex.json
Inverted Index of all topics to all the documents that contain them.
