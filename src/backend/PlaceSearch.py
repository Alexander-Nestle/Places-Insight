import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import EnglishStemmer
from backend.Config import Config
from backend.DataBase import DBManager
from backend.PlaceShow import PlaceShow
from backend.PlaceRank import Ranking


class ReviewItem:
    """This class defines the structure of one review item inside the Document"""
    def __init__(self, id, rating, time, review_text):
        self.id = id
        self.rating = rating
        self.time = time
        self.review_text = review_text


class PlaceSearch:
    """Place Search Algorithm"""
    def __init__(self, config):
        DBManager.initialize(config)
        self.index_db = DBManager.get_index_db()
        self.tokenizer = word_tokenize
        self.stemmer = EnglishStemmer()

        try:
            self.stopwords = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            nltk.download('punkt')
            self.stopwords = set(stopwords.words('english'))

    def load(self):
        """Load index and document json file and build index structure"""
        self.index_db.load_db()

    def search(self, query):
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
            cur_id_list = self.index_db.get_docs(word).keys()
            if len(doc_id_set) == 0:
                doc_id_set = set(cur_id_list)
            else:
                doc_id_set = doc_id_set.union(set(cur_id_list))

        return query_word_set, doc_id_set


class SearchRank:
    """
    This provide one-in-all interface to caller
    Including PlaceSearch, PlaceRank
    """
    def __init__(self, config):
        self.config = config
        self.plc_search = None
        self.plc_rank = None

    def initialize(self):
        self.plc_search = PlaceSearch(self.config)
        self.plc_search.load()
        self.plc_rank = Ranking(self.config)
        self.plc_rank.initialize()

    def search(self, query_str, max_shown=100):
        query_word_set, doc_id_set = self.plc_search.search(query_str)
        doc_list = self.plc_rank.ranking(doc_id_set, query_word_set)
        if len(doc_list) >= max_shown:
            return doc_list[0: max_shown]
        else:
            return doc_list


"""
Called when directly invoked
This is just for testing purpose
"""
if __name__ == "__main__":

    query_str = "child friendly restaurant"
    max_shown = 8
    show_counter = 0
    config = Config()

    """First, build a search object"""
    search_rank = SearchRank(config)
    search_rank.initialize()

    plc_show = PlaceShow(config)
    plc_show.load()

    query_doc_list = search_rank.search(query_str, max_shown)
    for query_item in query_doc_list:
        query_doc_item = query_item[0]
        print("=" * 20 + " Result " + str(show_counter) + " " + "=" * 20)
        print("BM25 score: " + str(query_item[1]))
        print("Document Key: " + str(query_item[0]))

        print(plc_show.show_text(str(query_item[0])))
        show_counter += 1
