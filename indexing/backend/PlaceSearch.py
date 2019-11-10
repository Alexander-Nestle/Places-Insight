import json
import math
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from backend.FileManager import FileManager


class DocumentCollection:
    """This class defines the structure that serves for all documents"""
    def __init__(self):
        self.doc_num = 0
        self.avg_dl = 0


class ReviewItem:
    """This class defines the structure of one review item inside the Document"""
    def __init__(self, id, rating, time, review_text):
        self.id = id
        self.rating = rating
        self.time = time
        self.review_text = review_text


class JsonIndexParser:
    """Parse the index document and load it to memory"""
    def __init__(self, index_file, doc_file):
        self.index_file = index_file
        self.doc_file = doc_file
        self.raw_index = defaultdict(list)
        self.doc_list = list()

    def load(self):
        with open(self.index_file, 'rb') as f2:
            self.raw_index = json.load(f2)
        with open(self.doc_file, 'rb') as f3:
            self.doc_list = json.load(f3)


class Ranking:
    """Ranking class"""
    def __init__(self, index_dict, doc_collection):
        self.index = index_dict
        self.doc_collection = doc_collection

    """Calculate the BM25 score of one query to a certain document"""
    def bm25(self, query, document, k1=1.2, b=0.75):
        """Note the query are provided in a tokenized manner"""
        score = 0
        for word in query:
            nq = len(self.index[word])
            idf = math.log2((self.doc_collection.doc_num - nq + 0.5) / (nq + 0.5))
            fqd = 0
            if document["id"] in self.index[word].keys():
                fqd = self.index[word][document["id"]]
            score += idf * fqd * (k1 + 1)/(fqd + k1 * (1 - b + b * document["len"] / self.doc_collection.avg_dl))
        return score

    """Perform the ranking"""
    def ranking(self, doc_ids, query, documents):
        doc_list = []
        for id in doc_ids:
            bm25_score = self.bm25(query, documents[id])
            doc_list.append([documents[id]["key"], bm25_score])
        """Sort by bm25 score"""
        doc_list.sort(key=lambda x: x[1], reverse=True)
        return doc_list


class PlaceShow:
    """
    This module is in charge of how/what to display to user based on returned document key
    This would take search doc key as input.
    The output would be send to frontend for display, this module may also be directly invoked in frontend
    """
    def __init__(self, ref_document):
        self.ref_doc = ref_document
        self.ref_dict = defaultdict()

    def load(self):
        with open(self.ref_doc, "rb") as f:
            data_doc_list = json.load(f)
            for doc in data_doc_list:
                self.ref_dict[doc["place_id"]] = doc

    def get_item(self, key):
        doc = self.ref_dict[key]
        return doc

    def show_text(self, key):
        doc = self.ref_dict[key]
        output = ""
        cnt = 1
        for rev in doc["reviews"]:
            output += "Review " + str(cnt) + ": " + rev["text"].strip() + "\n"
            cnt += 1
        return output


class PlaceSearch:
    """Place Search Algorithm"""
    def __init__(self, index_file, doc_file):
        self.index_file = index_file
        self.doc_file = doc_file
        self.tokenizer = word_tokenize
        self.stemmer = EnglishStemmer()
        self.index = defaultdict(dict)
        self.documents = list()
        """self.docmap = defaultdict()"""
        self.doc_collection = DocumentCollection()
        self.ranking = None
        try:
            self.stopwords = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            nltk.download('punkt')
            self.stopwords = set(stopwords.words('english'))

    """Load index and document json file and build index structure"""
    def load(self):
        # load parse index file
        index_parser = JsonIndexParser(self.index_file, self.doc_file)
        index_parser.load()
        for token in index_parser.raw_index.keys():
            doc_item_list = index_parser.raw_index[token]
            for doc_item in doc_item_list:
                self.index[token][doc_item["id"]] = doc_item["cnt"]
        # load and parse doc file
        self.documents = index_parser.doc_list
        total_len = 0
        cnt = 0
        for doc in self.documents:
            total_len += doc["len"]
            assert doc["id"] == cnt
            cnt += 1
        self.doc_collection.doc_num = len(self.documents)
        self.doc_collection.avg_dl = total_len / self.doc_collection.doc_num
        self.ranking = Ranking(self.index, self.doc_collection)

    def search(self, query, maxshown=100):
        """tokenize the query and run search for each token"""
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

        doc_list = self.ranking.ranking(doc_id_set, query_word_set, self.documents)
        if len(doc_list) >= maxshown:
            return doc_list[0: maxshown]
        else:
            return doc_list


"""Called when directly invoked"""
if __name__ == "__main__":

    query_str = "child friendly restaurant"
    max_shown = 8
    show_counter = 0
    fmanager = FileManager()
    data_file = fmanager.data_file
    index_file = fmanager.index_file
    doc_file = fmanager.doc_file

    """First, build a search object"""
    plc_search = PlaceSearch(index_file, doc_file)
    plc_search.load()

    plc_show = PlaceShow(data_file)
    plc_show.load()

    query_doc_list = plc_search.search(query_str, max_shown)
    for query_item in query_doc_list:
        query_doc_item = query_item[0]
        print("=" * 20 + " Result " + str(show_counter) + " " + "=" * 20)
        print("BM25 score: " + str(query_item[1]))
        print("Document Key: " + str(query_item[0]))
        """
        print("name: " + query_doc_item.name)
        print("address: " + query_doc_item.address)
        print("review: " + query_doc_item.review)
        """
        print(plc_show.show_text(str(query_item[0])))
        show_counter += 1