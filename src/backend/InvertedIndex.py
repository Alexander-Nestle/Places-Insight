import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from backend.Config import Config
from backend.DataBase import DBManager


class DocumentItem:
    """This class defines the structure of one touristic site, which is used indexing part"""
    def __init__(self, doc_id, key, reviews):
        self.id = doc_id
        self.key = key
        self.reviews = reviews
        self.doc_len = 1

    def serialize(self):
        """This is designed for saving to a json file"""
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
        item_text = ""
        for item_rev in item_raw['reviews']:
            if "language" in item_rev.keys() and item_rev["language"].lower() != "en":
                continue
            item_text += item_rev["text"]
            item_text += " "
        self.doc_idx += 1
        return DocumentItem(self.doc_idx-1, item_key, item_text)


class IndexItem:
    """Temporary definition for index item"""
    def __init__(self, doc_id, token_cnt):
        self.doc_id = doc_id
        self.token_cnt = token_cnt

    def serialize(self):
        """This is designed for saving to a json file"""
        ind_item_dict = dict()
        ind_item_dict["id"] = self.doc_id
        ind_item_dict["cnt"] = self.token_cnt
        return ind_item_dict


class InvertedIndex:
    """Class for inverted indexing, main class here"""
    def __init__(self, config):
        conf = config.conf
        self.input_file = config.path + conf["data_file"]
        assert self.input_file is not None
        self.meta_file = config.path + conf["meta_file"]
        assert self.meta_file is not None
        DBManager.initialize(config)
        self.index_db = DBManager.get_index_db()
        self.doc_db = DBManager.get_doc_db()
        self.tokenizer = word_tokenize
        self.stemmer = EnglishStemmer()
        self.doc_num = 0
        self.total_len = 0
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

            if not self.index_db.token_exist(token):
                self.index_db.put_token(token, IndexItem(doc_id, 1))
            elif self.index_db.token_doc_exist(token, doc_id):
                self.index_db.inc_token_cnt(token, doc_id)
            else:
                self.index_db.append_token(token, IndexItem(doc_id, 1))

        document.set_doclen(doc_len)
        self.doc_db.add_doc(document)
        self.doc_num += 1
        self.total_len += doc_len

    def save_index(self):
        """Save Index to a file"""
        self.index_db.save_db()

    def save_document(self):
        """Save document to a file"""
        self.doc_db.save_db()

    def save_meta(self):
        """Save metadata to a file"""
        meta_file_handler = open(self.meta_file, "w+")
        meta_data = dict()
        meta_data["doc_num"] = self.doc_num
        meta_data["avg_dl"] = self.total_len/self.doc_num
        json.dump(meta_data, meta_file_handler)

    def build_index(self):
        """Parse a json File"""
        jparser = JsonDocParser(self.input_file)
        jparser.parse()
        while jparser.has_more_item():
            doc_item = jparser.get_next_item()
            if doc_item is not None:
                self.add(doc_item)
        self.save_index()
        self.save_document()
        self.save_meta()


"""Called when directly invoked"""
if __name__ == "__main__":
    config = Config()
    invert_index = InvertedIndex(config)
    invert_index.build_index()
