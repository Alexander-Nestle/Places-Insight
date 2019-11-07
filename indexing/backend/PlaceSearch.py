import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from .JsonOps import JsonIndexParser
from .ReviewDocument import DocumentCollection
from .Ranking import Ranking

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
        self.ranking = Ranking(self.index, self.docCollection)


    """tokenize the query and run search for each token"""
    def search(self, query, maxshown=100):
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

    from indexing.backend.PlaceShow import PlaceShow

    query_str = "child friendly restaurant"
    max_shown = 8
    show_counter = 0
    oriDocFile = "dataset.json"
    indexFile = "dataindex.json"
    docFile = "datadoc.json"

    """First, build a search object"""
    plcSearch = PlaceSearch(indexFile, docFile)
    plcSearch.load()

    plcShow = PlaceShow(oriDocFile)
    plcShow.load()

    query_doc_list = plcSearch.search(query_str, max_shown)
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
        print(plcShow.show_text(str(query_item[0])))
        show_counter += 1