import math
import json
from backend.DataBase import DBManager


class Ranking:
    """Ranking class"""
    def __init__(self, config, index_db):
        """We assume that index_db is already created in indexing phase"""
        conf = config.conf
        self.index_db = index_db
        meta_file = config.path + conf["meta_file"]
        with open(meta_file, "r") as f:
            meta_data = json.load(f)
            self.doc_num = meta_data["doc_num"]
            self.avg_dl = meta_data["avg_dl"]
        db_manager = DBManager(config)
        self.doc_db = db_manager.get_doc_db()

    def initialize(self):
        """This is to load doc for ranking purpose"""
        self.doc_db.load_db()

    def bm25(self, query, document, k1=1.2, b=0.75):
        """Calculate the BM25 score of one query to a certain document"""
        """Note the query are provided in a tokenized manner"""
        score = 0
        for word in query:
            doc_list = self.index_db.get_docs(word)
            nq = len(doc_list)
            print("word is " + str(word))
            print("nq is " + str(nq))
            idf = math.log2((self.doc_num - nq + 0.5) / (nq + 0.5))
            fqd = 0
            if document["id"] in doc_list.keys():
                fqd = doc_list[document["id"]]
            score += idf * fqd * (k1 + 1)/(fqd + k1 * (1 - b + b * document["len"] / self.avg_dl))
        return score

    def ranking(self, doc_ids, query):
        """Perform the ranking"""
        doc_list = []
        for id in doc_ids:
            document = self.doc_db.get_doc(id)
            bm25_score = self.bm25(query, document)
            doc_list.append([document["key"], bm25_score])
        """Sort by bm25 score"""
        doc_list.sort(key=lambda x: x[1], reverse=True)
        return doc_list
