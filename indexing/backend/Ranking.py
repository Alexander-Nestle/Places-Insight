import math

"""Ranking class"""
class Ranking:
    def __init__(self, indexDict, docCollection):
        self.index = indexDict
        self.docCollection = docCollection

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

    """Perform the ranking"""
    def ranking(self, doc_ids, query, documents):
        doc_list = []
        for id in doc_ids:
            bm25_score = self.bm25(query, documents[id])
            doc_list.append([documents[id]["key"], bm25_score])
        """Sort by bm25 score"""
        doc_list.sort(key=lambda x: x[1], reverse=True)
        return doc_list
