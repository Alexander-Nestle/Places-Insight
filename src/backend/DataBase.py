"""
An interface and implementation of database operations
Here we suppose the implementation of indexing and searching are done through DB operations
At the initial phase, we implement the DB through in-memory DB
If time permit, we can consider using DB like MongoDB
"""
from abc import abstractmethod, ABCMeta
import json
from collections import defaultdict


class IndexDBInterface(metaclass=ABCMeta):
    """ Abstract class for Index DataBase"""

    @abstractmethod
    def put_token(self, token, index_item):
        pass

    @abstractmethod
    def append_token(self, token, index_item):
        pass

    @abstractmethod
    def inc_token_cnt(self, token, doc_id):
        pass

    @abstractmethod
    def token_exist(self, token):
        pass

    @abstractmethod
    def token_doc_exist(self, token, doc_id):
        pass

    @abstractmethod
    def save_db(self):
        pass

    @abstractmethod
    def load_db(self):
        pass

    @abstractmethod
    def get_docs(self, token):
        pass


class IndexMemoryDB(IndexDBInterface):
    """ Implementation of Index DB through Memory"""
    def __init__(self, index_file):
        self.index_file = index_file
        """index is used for indexing phase, while index2 is used for search phase"""
        self.index = defaultdict(list)
        self.index2 = defaultdict(dict)

    """This and following defined for indexing phase"""
    def put_token(self, token, index_item):
        self.index[token].append(index_item)

    def append_token(self, token, index_item):
        self.index[token].append(index_item)

    def inc_token_cnt(self, token, doc_id):
        assert doc_id == self.index[token][-1].doc_id
        self.index[token][-1].token_cnt += 1

    def get_token(self, token):
        return self.index[token]

    def token_exist(self, token):
        return len(self.get_token(token)) != 0

    def token_doc_exist(self, token, doc_id):
        if not self.token_exist(token):
            return False
        else:
            return self.get_token(token)[-1].doc_id == doc_id

    def save_db(self):
        index_file_handler = open(self.index_file, "w+")
        json.dump(self.index, index_file_handler, default=lambda x: x.serialize())

    """This and following defined for searching phase"""
    def load_db(self):
        index_file_handler = open(self.index_file, "r")
        raw_index = json.load(index_file_handler)
        for token in raw_index.keys():
            doc_item_list = raw_index[token]
            for doc_item in doc_item_list:
                self.index2[token][doc_item["id"]] = doc_item["cnt"]

    def get_docs(self, token):
        return self.index2[token]


class DocumentDBInterface(metaclass=ABCMeta):
    """Abstract class of Document Database"""

    @abstractmethod
    def add_doc(self, doc_item):
        pass

    @abstractmethod
    def save_db(self):
        pass

    @abstractmethod
    def load_db(self):
        pass

    @abstractmethod
    def get_doc(self, doc_id):
        pass


class DocumentMemoryDB(DocumentDBInterface):
    """Implementation of Document DB through Memory"""

    def __init__(self, doc_file):
        self.doc_file = doc_file
        self.documents = list()

    """This and following used for indexing phase"""
    def add_doc(self, doc_item):
        self.documents.append(doc_item)

    def save_db(self):
        doc_file_handler = open(self.doc_file, "w+")
        json.dump(self.documents, doc_file_handler, default=lambda x: x.serialize())

    """This and following used for searching phase"""
    def load_db(self):
        doc_file_handler = open(self.doc_file, "r")
        self.documents = json.load(doc_file_handler)

    def get_doc(self, doc_id):
        assert self.documents[doc_id]["id"] == doc_id
        return self.documents[doc_id]


class DBManager:
    """
    This is used to instantiate DB operation Class
    Implementation will change if we change DB Type
    Say from MemoryDB to MongoDB
    """
    index_db = None
    doc_db = None
    config = None
    path = ""
    initialized = False

    @classmethod
    def initialize(cls, config):
        if not cls.initialized:
            cls.config = config
            cls.path = config.path
        cls.initialized = True

    @classmethod
    def set_path(cls, relative_path):
        """
        This is designed for memorydb
        In considering app.py and InvertedIndex.py may be called with different path
        """
        cls.path = relative_path

    @classmethod
    def get_index_db(cls):
        if cls.index_db is None:
            db_type = cls.config.conf["db_type"]
            if db_type.lower() == "memorydb":
                index_file = cls.config.conf["index_file"]
                assert index_file is not None
                index_file = cls.path + index_file
                cls.index_db = IndexMemoryDB(index_file)
        return cls.index_db

    @classmethod
    def get_doc_db(cls):
        if cls.doc_db is None:
            db_type = cls.config.conf["db_type"]
            if db_type.lower() == "memorydb":
                doc_file = cls.config.conf["doc_file"]
                assert doc_file is not None
                doc_file = cls.path + doc_file
                cls.doc_db = DocumentMemoryDB(doc_file)
        return cls.doc_db

