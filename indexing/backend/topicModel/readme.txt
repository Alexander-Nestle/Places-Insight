*** File Descriptions ***

Model Directory - Contains the generated topic model.  Gensim library can readin these files to produce a lda_model object.  
                  Code to do this can be found in topicmodel.py

preprocessd_reviews - Contains preprocessed reviews for LDA model (linting, stemming, etc)

pyLDAvis.html - HTML file that allows for a detailed visualization for the topics.  NOTE: topic numbers in visualization do not correlate
                with topics from model/json file.

topicmodel.py - All the code needed for generating topic model using LDA

topics.json - Contains all topics and the word distributions

