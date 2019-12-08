import math
import json
from backend.DataBase import DBManager
from backend.topicModel.TopicModelService import TopicModelService


class Ranking:
    """Ranking class"""
    def __init__(self, config):
        """We assume that index_db is already created in indexing phase"""
        conf = config.conf
        assert DBManager.initialized is True
        self.index_db = DBManager.get_index_db()
        meta_file = config.path + conf["meta_file"]
        with open(meta_file, "r") as f:
            meta_data = json.load(f)
            self.doc_num = meta_data["doc_num"]
            self.avg_dl = meta_data["avg_dl"]
        self.doc_db = DBManager.get_doc_db()
        self.topic_model_service = TopicModelService('./backend/topicModel/model/model', './backend/topicModel/preprocessed_reviews.txt', './backend/topicModel/topicInvertedIndex.json')

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
            idf = math.log2((self.doc_num - nq + 0.5) / (nq + 0.5))
            fqd = 0
            if document["id"] in doc_list.keys():
                fqd = doc_list[document["id"]]
            score += idf * fqd * (k1 + 1)/(fqd + k1 * (1 - b + b * document["len"] / self.avg_dl))
        return score

    def ranking(self, doc_ids, query):
        """Perform the ranking"""
        # Classifies Query to topic
        query_topic = self.topic_model_service.get_query_topic(query)

        doc_list = []
        for id in doc_ids:
            document = self.doc_db.get_doc(id)
            # BM25 Score
            bm25_score = self.bm25(query, document)

            # Topic Score
            if query_topic != -1:
                topic_model_score = self.topic_model_service.topic_score(query_topic, document["key"])
            else:
                topic_model_score = 1

            # Combines Topic Score and BM25 Score
            score = topic_model_score * bm25_score

            doc_list.append([document["key"], score])
        """Sort by bm25 score"""
        doc_list.sort(key=lambda x: x[1], reverse=True)
        return doc_list
