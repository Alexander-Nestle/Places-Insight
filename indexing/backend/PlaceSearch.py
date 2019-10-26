import nltk
import math
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from indexing.backend.ReviewDocument import DocumentCollection
from indexing.backend.JsonOps import JsonIndexParser

"""Place Search Algorithm"""
class PlaceSearch:
    def __init__(self, indexFile, docFile):
        self.indexFile = indexFile
        self.docFile = docFile
        self.tokenizer = word_tokenize
        self.stemmer = EnglishStemmer()
        self.index = defaultdict(dict)
        self.documents = list()
        self.docmap = defaultdict()
        self.docCollection = DocumentCollection()
        try:
            self.stopwords = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            nltk.download('punkt')
            self.stopwords = set(stopwords.words('english'))

    """Load index and document json file and build index structure"""
    def load(self):
        # load parse index file
        indexParser = JsonIndexParser(self.indexFile, self.docFile)
        indexParser.load()
        for token in indexParser.rawIndex.keys():
            docItemList = indexParser.rawIndex[token]
            for docItem in docItemList:
                self.index[token][docItem["id"]] = docItem["cnt"]
        # load and parse doc file
        self.documents = indexParser.doclist
        total_len = 0
        cnt = 0
        for doc in self.documents:
            total_len += doc["len"]
            assert doc["id"] == cnt
            cnt += 1
        self.docCollection.doc_num = len(self.documents)
        self.docCollection.avg_dl = total_len/self.docCollection.doc_num

    """Calculate the BM25 score of one query to a certain document"""
    def bm25(self, query, document, k1=1.2, b=0.75):
        """Note the query are provided in a tokenized manner"""
        score = 0
        for word in query:
            nq = len(self.index[word])
            idf = math.log2((self.docCollection.doc_num - nq + 0.5)/(nq + 0.5))
            fqd = 0
            if document["id"] in self.index[word].keys():
                fqd = self.index[word][document["id"]]
            score += idf * fqd * (k1 + 1)/(fqd + k1 * (1 - b + b * document["len"]/self.docCollection.avg_dl))
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
        doc_id_set = set()
        for word in query_word_set:
            cur_id_list = self.index.get(word).keys()
            if len(doc_id_set) == 0:
                doc_id_set = set(cur_id_list)
            else:
                doc_id_set = doc_id_set.union(set(cur_id_list))

        """retrieve document content"""
        doc_list = []
        for id in doc_id_set:
            bm25_score = self.bm25(query_word_set, self.documents[id])
            doc_list.append([self.documents[id]["key"], bm25_score])

        """Sort by bm25 score"""
        doc_list.sort(key=lambda x: x[1], reverse=True)
        if len(doc_list) >= maxshown:
            return doc_list[0: maxshown]
        else:
            return doc_list