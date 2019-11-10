import json
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from backend.FileManager import FileManager


class DocumentItem:
    """This class defines the structure of one touristic site, which is used indexing part"""
    def __init__(self, doc_id, key, name, address, reviews):
        self.id = doc_id
        self.key = key
        self.name = name
        self.address = address
        self.reviews = reviews
        self.doc_len = 1

    def serialize(self):
        doc_item_dict = dict()
        doc_item_dict["id"] = self.id
        doc_item_dict["key"] = self.key
        doc_item_dict["len"] = self.doc_len
        return doc_item_dict

    def set_doclen(self, doc_len):
        """Set document length, note this length are counted in words and have stop words removed"""
        self.doc_len = doc_len


class JsonDocParser:
    """parse the review documents into documentItems"""
    def __init__(self, filename):
        self.filename = filename
        self.doc_list = []
        self.doc_idx = 0

    def parse(self):
        with open(self.filename, 'rb') as f:
            self.doc_list = json.load(f)

    def has_more_item(self):
        return self.doc_idx < len(self.doc_list)

    def get_next_item(self):
        if len(self.doc_list) == 0:
            print("Error: need to parse before getitem")
            return
        if self.doc_idx >= len(self.doc_list):
            print("Error: index has exceeded maximum item numbers")
            return
        item_raw = self.doc_list[self.doc_idx]
        item_key = item_raw['place_id']
        item_name = item_raw['name']
        item_address = item_raw['formatted_address']
        item_text = ""
        for item_rev in item_raw['reviews']:
            if "language" in item_rev.keys() and item_rev["language"].lower() != "en":
                continue
            item_text += item_rev["text"]
            item_text += " "
        self.doc_idx += 1
        return DocumentItem(self.doc_idx-1, item_key, item_name, item_address, item_text)


class IndexItem:
    """Temporary definition for index item"""
    def __init__(self, doc_id, token_cnt):
        self.doc_id = doc_id
        self.token_cnt = token_cnt

    def serialize(self):
        ind_item_dict = dict()
        ind_item_dict["id"] = self.doc_id
        ind_item_dict["cnt"] = self.token_cnt
        return ind_item_dict


class InvertedIndex:
    """Class for inverted indexing, main class here"""
    def __init__(self, input_file, index_file, doc_out_file):
        self.input_file = input_file
        self.index_file = index_file
        self.doc_file = doc_out_file
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
        doc_text = document.reviews
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
            elif self.index[token][-1].doc_id == doc_id:
                self.index[token][-1].token_cnt += 1
            else:
                self.index[token].append(IndexItem(doc_id, 1))

        document.set_doclen(doc_len)
        self.documents.append(document)

    """Save Index to a file"""
    def save_index(self):
        index_file_handler = open(self.index_file, "w+")
        json.dump(self.index, index_file_handler, default=lambda x: x.serialize())

    """Save document to a file"""
    def save_document(self):
        doc_file_handler = open(self.doc_file, "w+")
        json.dump(self.documents, doc_file_handler, default=lambda x: x.serialize())

    """Parse a json File"""
    def build_index(self):
        jparser = JsonDocParser(self.input_file)
        jparser.parse()
        while jparser.has_more_item():
            doc_item = jparser.get_next_item()
            if doc_item is not None:
                self.add(doc_item)
        self.save_index()
        self.save_document()


"""Called when directly invoked"""
if __name__ == "__main__":

    fmanager = FileManager()
    input_file = fmanager.data_file
    index_file = fmanager.index_file
    document_file = fmanager.doc_file
    invert_index = InvertedIndex(input_file, index_file, document_file)
    invert_index.build_index()
