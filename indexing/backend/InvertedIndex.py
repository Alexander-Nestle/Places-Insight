import json
import nltk
import math
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from backend.ReviewDocument import DocumentCollection,DocumentItem
from backend.JsonOps import JsonParser


class InvertedIndex:
    def __init__(self, inputFile, indexFile, docOutFile):
        self.inputFile = inputFile
        self.indexFile = indexFile
        self.docFile = docOutFile
        self.tokenizer = word_tokenize
        self.stemmer = EnglishStemmer()
        self.index = defaultdict(dict)
        self.documents = dict()
        self.docCollection = DocumentCollection()
        try:
            self.stopwords = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            nltk.download('punkt')
            self.stopwords = set(stopwords.words('english'))

    """indexing a document item"""
    def add(self, document):
        """Retrieve document key and content"""
        doc_key = document.key
        # doc_name = document.name
        doc_text = document.review
        doc_len = 0

        for token in self.tokenizer(doc_text):
            token = token.lower()
            if token in self.stopwords:
                continue

            doc_len += 1
            if self.stemmer:
                token = self.stemmer.stem(token)

            if doc_key not in self.index[token]:
                self.index[token][doc_key] = 1
            else:
                self.index[token][doc_key] += 1

        self.documents[doc_key] = document
        document.set_doclen(doc_len)
        self.docCollection.add_doc(doc_len)

    """Save Index to a file"""
    def saveIndex(self):
        indexFileHandler = open(self.indexFile, "w+")
        json.dump(self.index, indexFileHandler, default=lambda x: x.keys())

    """Save document to a file"""
    def saveDocument(self):
        docFileHandler = open(self.docFile, "w+")
        json.dump(self.documents, docFileHandler, default=lambda x: x.my_serialize())

    """Parse a json File"""
    def buildIndex(self):
        jParser = JsonParser(self.inputFile)
        jParser.parse()
        while jParser.has_more_item():
            docItem = jParser.get_next_item()
            if docItem != None:
                self.add(docItem)
        self.saveIndex()
        self.saveDocument()


    """Calculate the BM25 score of one query to a certain document"""
    def bm25(self, query, document, k1=1.2, b=0.75):
        """Note the query are provided in a tokenized manner"""
        score = 0
        for word in query:
            nq = len(self.index[word])
            idf = math.log2((self.docCollection.doc_num - nq + 0.5)/(nq + 0.5))
            fqd = 0
            if document.key in self.index[word]:
                fqd = self.index[word][document.key]
            score += idf * fqd * (k1 + 1)/(fqd + k1 * (1 - b + b * document.doc_len/self.docCollection.avg_dl))
        return score

    """tokenize the query and run search for each token"""
    def search(self, query, maxshown=10):
        """first, process the query string"""
        query_words = self.tokenizer(query)
        query_word_set = set()
        for word in query_words:
            word = word.lower()
            if word in self.stopwords:
                continue
            if self.stemmer:
                word = self.stemmer.stem(word)
            query_word_set.add(word)

        """second, for each unique word,run query"""
        doc_key_set = set()
        for word in query_word_set:
            if len(doc_key_set) == 0:
                doc_key_set = set(self.index.get(word).keys())
            else:
                doc_key_set = doc_key_set.union(set(self.index.get(word).keys()))

        """retrieve document content"""
        doc_list = []
        for key in doc_key_set:
            bm25_score = self.bm25(query_word_set, self.documents[key])
            doc_list.append([self.documents[key], bm25_score])

        """Sort by bm25 score"""
        doc_list.sort(key=lambda x: x[1], reverse=True)
        if len(doc_list) >= maxshown:
            return doc_list[0: maxshown]
        else:
            return doc_list