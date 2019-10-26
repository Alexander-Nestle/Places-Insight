import json
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from indexing.backend.JsonOps import JsonDocParser

"""Tempory defininition for index item"""
class IndexItem:
    def __init__(self, docId, tokenCnt):
        self.docId = docId
        self.tokenCnt = tokenCnt

    def serialize(self):
        indItemDict = dict()
        indItemDict["id"] = self.docId
        indItemDict["cnt"] = self.tokenCnt
        return indItemDict

"""Class for inverted index"""
class InvertedIndex:
    def __init__(self, inputFile, indexFile, docOutFile):
        self.inputFile = inputFile
        self.indexFile = indexFile
        self.docFile = docOutFile
        self.tokenizer = word_tokenize
        self.stemmer = EnglishStemmer()
        self.index = defaultdict(list)
        self.documents = list()
        try:
            self.stopwords = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            nltk.download('punkt')
            self.stopwords = set(stopwords.words('english'))

    """indexing a document item"""
    def add(self, document):
        """Retrieve document id and content"""
        doc_id = document.id
        doc_text = document.review
        doc_len = 0

        for token in self.tokenizer(doc_text):
            token = token.lower()
            if token in self.stopwords:
                continue

            doc_len += 1
            if self.stemmer:
                token = self.stemmer.stem(token)

            if len(self.index[token]) == 0:
                self.index[token].append(IndexItem(doc_id, 1))
            elif self.index[token][-1].docId == doc_id:
                self.index[token][-1].tokenCnt += 1
            else:
                self.index[token].append(IndexItem(doc_id, 1))

        document.set_doclen(doc_len)
        self.documents.append(document)

    """Save Index to a file"""
    def saveIndex(self):
        indexFileHandler = open(self.indexFile, "w+")
        json.dump(self.index, indexFileHandler, default=lambda x: x.serialize())

    """Save document to a file"""
    def saveDocument(self):
        docFileHandler = open(self.docFile, "w+")
        json.dump(self.documents, docFileHandler, default=lambda x: x.serialize())

    """Parse a json File"""
    def buildIndex(self):
        jParser = JsonDocParser(self.inputFile)
        jParser.parse()
        while jParser.has_more_item():
            docItem = jParser.get_next_item()
            if docItem != None:
                self.add(docItem)
        self.saveIndex()
        self.saveDocument()
