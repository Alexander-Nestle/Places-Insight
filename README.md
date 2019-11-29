# Places Insights
### Natural Language Search Engine for Places
Final Project for CS410: Text Information Analytics at the University of Illinois at Urbana-Champaign
Akhmad Rahadian Hutomo, ahutomo2@illinois.edu | Alexander Nestle, nestle2@illinois.edu | Eric Yang Liu, yangl18@illinois.edu

## 1. Software Overview

An overview of the function of the code 

### 1.1 What it does?

The goal of this project is to create a search engine implementation that will allow users to query a database of businesses, places, and parks (which will be referred to as ‘places’ within this document) using natural language attributes such as ‘child friendly’, ‘Italian food’, or ‘beautiful building’ in order to quickly receive relevant places

![](@attachment/Clipboard_2019-11-29-16-11-47.png)

User will be interfacing with a query input that will predict the relevant places based on the query itself and a set of topic based on the query

### 1.2 Use Case

User may enter query based on variety of use case. The goals of the software is to recieve a natural language query and predict the most likely based on user intent. 

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

Currently, the place names and addresses were scraped from Facebook travel page recommendations, which were then used to query the Google Places API to receive place information and reviews. We may also collect more place/reviews from different sources (say, yelp, Kaggle) for any upcoming iterations of projects.

Topic modeling will be used to create the ‘queryable attributes’ of the places. This will be done by running the topic modeling algorithm (say LDA algorithm) against all the collected reviews. This will create the queryable topics (place attributes). During the topic modeling process, we will need to manually interpret the topics and name them appropriately.

Once the topics are created, we will run each review through our topic model. This will tell us the topics that each review included, and the most common topics will be used to describe each place, which is then queryable by the user.

### 2.2 Web Front End - View

### 2.3 Indexing and Search Module

This module is the back end implementation of indexing and query, it contains following part:

1. Config file
2. Indexing Module
3. Query Module
4. Display Content Module
5. Database Module (To be designed)

#### 2.3.1 Configuration

This is defined with config.json and Config.py

The purpose of using configuration file is:

1. To define the database type (memoryDB, mongoDB, etc)
2. If using memoryDB, define which files it is written to.

#### 2.3.2 Indexing

This is implemented through file `InvertedIndex.py`

##### Input:

The scraped json file standing for the geographic data, this file comes from Alex

##### Output:

1. One output indexing file in json format, which is the first layer mapping from a token to a list of documents(save document id or document key)

2. Another output file which maps the document id (or document key) to document key

#### Algorithm:

Use inverted indexing to create indexing from input json file.

#### Design consideration:

Here we save in the first json file the document ID (from read ordering) iso document key just to save space

### 2.3.3 Search

This is implemented through `PlaceSearch.py`

There are two steps:

* First, we load the indexing file in json format
* Second, we process user query

#### Loading Phase:

##### Input:

The indexing file in json format obtained from `Indexing` step

##### Output:

A in memory database of the indexing table/map

#### Query Phase:

##### Input:

The query string

##### Output:

The Key to the document

##### Algorithm:

1. Run query on each token and come up with a combined query result

2. Run ranking function and return query results (doc_key), ranking function used here is BM25


### 2.3.4 Show

Implemented through `PlaceShow.py`

Display result based on document key

#### Algorithm:

Query the document specifics based on the doc key

Display the result, the format can be customized and adjusted

#### Design consideration

The mapping between doc key and documents can be designed either through json file or mongoDB

### 2.3.5 DataBase Module

Implemented through DataBase.py

Currently only implemented with DB interface and MemoryDB as instance

### 2.3.6 How to test Search & Indexing implementation

1. Directly Run `python InvertedIndex.py` to create Index:
   1. Note we need to copy `PlacesResults.json` in the same directory
2. Directly Run `python PlaceSearch.py` to search from a predefined query string

### 2.4 Topic Modelling

### 2.5 Other 

#### 2.5.1 Query Expansion

#### 2.5.2 Word Embedding

#### 2.5.3 Pseudo Relevance Feedback

### 2.6 Future extension and improvement

- Expand the dataser or test on different dataset
- Performance measurement of the software compared to other available services
- Test and find suitable ranking algorithm 
- Explore different topic model parameters
- Explore on query expansions
- Improving search result based on user feedback
- Open API to be used by other organization

## 3. Software Usage
Documentation of the usage of the software including either documentation of usages of APIs or detailed instructions on how to install and run a software

### 3.1 Prerequisites

1. Install required python modules
```
pip install x y z
```

2. Download required packages & resources

3. Run Server Applications 
```
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
- Dataset collection
- Data cleansing & preprocessing
- Web Front End implementation
- Topic modeling implementation
- Topic model & ranking function integration and 
- Project proposal preparation, project documentation

#### Yang Eric Liu - yangl18@illinois.edu
- Inverted index implementation
- Search function implementation
- Ranking function implementation
- Database implementation
- Code refactoring
- Project proposal preparation, project documentation
