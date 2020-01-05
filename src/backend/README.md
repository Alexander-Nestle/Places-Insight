# Indexing and Search Module



This module is the back end implementation of indexing and query, it contains following part:

1. Config file
2. Indexing Module
3. Query Module
4. Display Content Module
5. Database Module (To be designed)



### Configuration

This is defined with config.json and Config.py

The purpose of using configuration file is:

1. To define the database type (memoryDB, mongoDB, etc)
2. If using memoryDB, define which files it is written to.



### Indexing

This is implemented through file `InvertedIndex.py`

#### Input:

The scraped json file standing for the geographic data, this file comes from Alex

#### Output:

1. One output indexing file in json format, which is the first layer mapping from a token to a list of documents(save document id or document key)
2. Another output file which maps the document id (or document key) to document key

#### Algorithm:

Use inverted indexing to create indexing from input json file.

#### Design consideration:

Here we save in the first json file the document ID (from read ordering) iso document key just to save space



### Search

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


### Show

Implemented through `PlaceShow.py`

Display result based on document key

#### Algorithm:

Query the document specifics based on the doc key

Display the result, the format can be customized and adjusted

#### Design consideration

The mapping between doc key and documents can be designed either through json file or mongoDB



### DataBase Module

Implemented through DataBase.py

Currently only implemented with DB interface and MemoryDB as instance



### How to test

1. Directly Run `python InvertedIndex.py` to create Index:
   1. Note we need to copy `PlacesResults.json` in the same directory
2. Directly Run `python PlaceSearch.py` to search from a predefined query string

