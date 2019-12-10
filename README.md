# Places Insights
### Natural Language Search Engine for Places
Final Project for CS410: Text Information Analytics at the University of Illinois at Urbana-Champaign

Akhmad Rahadian Hutomo, ahutomo2@illinois.edu | Alexander Nestle, nestle2@illinois.edu | Eric Yang Liu, yangl18@illinois.edu

## 1. Software Overview

An overview of the function of the code 

### 1.1 What it does?

The goal of this project is to create a search engine implementation that will allow users to query a database of businesses, places, and parks (which will be referred to as ‘places’ within this document) using natural language attributes such as ‘child friendly’, ‘Italian food’, or ‘beautiful building’ in order to quickly receive relevant places

User will be interfacing with a query input.  The user entered query will then be run through a BM25 ranking algorithm that includes topic model weighting to return ranked relevant places to the user.

### 1.2 Use Case

User may enter query based on variety of use cases. The goals of the software is to receive a natural language query and predict the most likely result based on user intent. 

Here are some possible use cases from users:

1. Search by place of interest: park, library
2. Search by business type: coffee shop, thai restaurant
3. Search by use case: child-friendly Italian restaurant
4. Search by activity: hiking, surfing
5. Search by object: latte, jazz, toys

Other query may return the most relevant places based on the keyword, or may not return any places at all.

The possible end user of this software may includes visitor or local resident of a certain place that looking for places recommendation. As this software provides basic functionality of searching places by natural languages, organizations such as regional government or business place owner may also reuse the software based on specific use case

## 2. Software Implementation
Documentation of how the software is implemented with sufficient detail so that others can have a basic understanding of your code for future extension or any further improvement.

### 2.1 Dataset

Currently, the place names and addresses were scraped from Facebook travel page recommendations, which were then used to query the Google Places API to receive place information and reviews. The other possible data source including collecting more place/reviews from different sources (say, yelp, Kaggle) for any upcoming iterations of projects. 

The storage of the database was initially designed through a simple json file. To enhance it further, developer can change it to NoSQL database if the volume of data increases during project implementation and enhancement.

A few data cleansing tasks has been done to the initial dataset to ensure there are no duplicates of places/ business entries, the place has a certain threshold of number of reviews and also count of the words inside the reviews.

The dataset information was expanded by using topic modeling to create the ‘queryable attributes’ of the places, which was added to each place in the dataset under the 'review_topics' key. 

Dataset Sample:
```
{
  "formatted_address": "Brooklyn, NY 11201, USA",
  "geometry": {
    "location": {
      "lat": 40.6896147,
      "lng": -73.9858984
    },
    "viewport": {
      "south": 40.6882965197085,
      "west": -73.9872249802915,
      "north": 40.6909944802915,
      "east": -73.98452701970848
    }
  },
  "name": "Brooklyn",
  "place_id": "ChIJq1RGWExawokRC5VK08ax-Ds",
  "reviews": [
    {
      "author_name": "hisham nofal",
      "author_url": "https://www.google.com/maps/contrib/114083506813599492082/reviews",
      "language": "en",
      "profile_photo_url": "https://lh3.ggpht.com/-2hGHNr4CZDQ/AAAAAAAAAAI/AAAAAAAAAAA/CN_PCdB3E8E/s128-c0x00000000-cc-rp-mo-ba6/photo.jpg",
      "rating": 4,
      "relative_time_description": "11 months ago",
      "text": "For bus is good",
      "time": 1538667162
    }
  ],
  "types": [
    "transit_station",
    "point_of_interest",
    "establishment"
  ],
  "url": "https://maps.google.com/?cid=4321399309968512267",
  "html_attributions": []
}ß

```

### 2.2 Web Front End - View

The front end is comprised of html templates which are dynamically served by the Flask framework.  These templates are styled using Bootstrap CSS, which has a JQuery dependency.

### 2.3 Indexing and Search Module

This module is the back end implementation of indexing and query, it contains following part:

1. Config file
2. Indexing Module
3. Query Module
4. Ranking Module
5. Display Content Module
6. Database Module (To be designed)

#### 2.3.1 Configuration

This is defined with config.json and Config.py

The purpose of using configuration file is:

1. To define the database type (memoryDB, mongoDB, etc)
2. If using memoryDB (in memory database), define source file (in json format) it is read from and the destination file it is written to (json file)

#### 2.3.2 Indexing

This is implemented through file `InvertedIndex.py`

##### Input:

The scraped json file stands for the geographic data, this file comes from Alex by scraping from Facebook travel recommendations

##### Output:

1. One output indexing file in json format, which is the first layer mapping from a token to a list of documents (save document id or document key) containing the token.

2. Another output file which maps the document id (or document key) to document key, with document(review) length for which will be used in ranking

#### Algorithm:

Use inverted indexing to do token indexing from input json file.

#### Design consideration:

Here we save in the first json file the document ID (from read ordering, incremented from 0) iso document key just to save space

### 2.3.3 Search

This is implemented through `PlaceSearch.py`

There are two steps:

* First, we load the indexing file in json format (we only load this once)
* Second, we process user query (run this for each query)

#### Loading Phase:

##### Input:

The indexing file in json format obtained from `Indexing` step

##### Output:

An in memory database of the indexing table/map

#### Query Phase:

##### Input:

The query string

##### Output:

The Keys to a list of documents matching the query string.

##### Algorithm:

1. Run query on each token and come up with a combined query result

2. Run ranking function and return query results (doc_key), ranking function used here is BM25 with topic  weight.

### 2.3.4 Ranking

The Ranking function is implemented through `PlaceRank.py`

It is singled out from search module in consideration of customizing purpose

#### Input:

1. Indexing file (dataindex.json) generated from Indexing phase
2. doc file (containing document meta info, say length) generated from indexing phase
3. topic modeling score (from query) generated from query 

#### Output:

1. A list of result in the order of ranking score (descending)

#### Algorithm:

1. Calculate the score of each query result using BM25
2. Calculate the topic score based on query topic (inferred from query string) and document topic;
3. Generate a weighted BM25 output. The BM25 score is weighted by a topic model score. The topic model score is calculated by first classifying the query and taking the ratio of how many reviews of the place mention the query topic (c) over the total number of reviews (n).  The final weighted score is (1 + (c/n)) * BM25.

### 2.3.5 Show

Implemented through `PlaceShow.py`

Display result based on document key

#### Algorithm:

Query the document specifics based on the doc key

Display the result, the format can be customized and adjusted

#### Design consideration

The mapping between doc key and documents can be designed either through json file or mongoDB

Currently, PlaceShow.py provide a standalone result show functionality for debugging purpose as well as interface for front end display.

### 2.3.6 DataBase Module

Implemented through DataBase.py

Currently only implemented with DB interface and MemoryDB as instance

### 2.3.7 How to test Search & Indexing implementation

1. Directly Run `python InvertedIndex.py` to create Index:
   1. Note we need to copy `PlacesResults.json` in the same directory
2. Directly Run `python PlaceSearch.py` to search from a predefined query string

### 2.4 Topic Modeling

The topic model was created using the LDA algorithm provided by the Gensim library over all of the reviews within the dataset.  A topic count of 40 was determined through empirical testing and the pyLDAvis library which provides a visual for topic coverage and overlap.  Code for the topic model generation can be found in TopicModelGenerator.py.

The topic model was used to expand the dataset by adding a count of the review topics to each place and provide weighting to the BM25 ranking. The topic model weighting score is calculated by first classifying the query and taking the ratio of how many reviews of the place mention the query topic (c) over the total number of reviews (n).  The final weighted score is (1 + (c/n)) * BM25.  Code for topic model utilization can be found in TopicModelService.py.

### 2.5 Other 

#### 2.5.1 Query Expansion
Project member has experimented using query expansion using Word2Vec word embedding function in Gensim module. The function first will be trained for reviews to create word vectors. Result then will be saved into a *.kv key vector file. Then, the query expansion will look for similar word based on the vectors. The top N similar word then will be added to original query.

The inital intention of having query expansion was to enhance search result for a single word query. However, after observation, the function will expand query with paradigmatic relation. This implementation may not work well for a specific search, for example: searching "Japan" will expand the query to "Japan Philadelphia Buddhist"

Possible improvement could be using syntagmatic relation function, or train the data using more generic corpus.

#### 2.5.2 Pseudo Relevance Feedback
Other experiment we tested was implementing pseudo relevance feedback. This implemented by running original ranking function (BM25), then take top N result, then take topic for this top N model, and expand that to the original query. After testing we found that the topic word was usually more generic/ background word, therefore did not further enhance query function.s


### 2.6 Future extension and improvement

- Expand the dataset or test on different dataset
- Using more scalable database, such as NoSQL DB
- Performance measurement of the software compared to other available services
- Test and find suitable ranking algorithm 
- Explore different topic model parameters
- Explore on query expansions
- Improving search result based on user feedback
- Open API to be used by other organization

## 3. Software Usage
Documentation of the usage of the software including either documentation of usages of APIs or detailed instructions on how to install and run a software

### 3.1 Prerequisites

Note: Application should be run with Python 3.

1. Install required python modules
```
pip install flask

pip install nltk

pip install gensim

pip install spacy

python -m spacy download en

pip install pyLDAvis
```

2. Download required packages & resources

3. Run Server Applications 
```
cd ./src
python app.py
```

4. Using web browser, launch http://127.0.0.1:5000/
Note: Supported Browser

Alternatively, we also provide services through this URL:

## 4. Team contribution
Brief description of contribution of each team member in case of a multi-person team

#### Akhmad Rahadian Hutomo - ahutomo2@illinois.edu
- Experiment on word embedding, combining topic modelling and ranking
- Query Expansion
- Project proposal preparation, project documentation
- Project presentation

#### Alexander Nestle - nestle2@illinois.edu
- Dataset scraping collection
- Data cleansing & preprocessing
- Web Front End implementation
- Topic modeling implementation
- Topic model & ranking function integration
- Project proposal preparation, project documentation

#### Yang Eric Liu - yangl18@illinois.edu
- Inverted index implementation
- Search function implementation
- Ranking function implementation
- Database implementation
- Code refactoring
- Project proposal preparation, project documentation
