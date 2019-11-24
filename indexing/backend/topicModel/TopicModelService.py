
import gensim
from backend.topicModel.JsonIO import JsonIO
from backend.topicModel.TopicModelGenerator import TopicModelGenerator 

class TopicModelService:
    """Class Performs Topic Model Services on Pregenerated Topic Model"""
    def __init__(self, model_path, model_corpus_path, inverted_index_path):
        self.topicModelGenerator = TopicModelGenerator()
        self.model_corpus = JsonIO.read_lst(model_corpus_path)
        self.dictionary = gensim.corpora.Dictionary(self.model_corpus)
        self.lda_model = gensim.models.LdaModel.load(model_path)
        self.topicInvertedIndex = JsonIO.read_json_file(inverted_index_path)
        
    def get_query_topic(self, query):
        """Classifies Query to Topic in Model"""
        # Generates token set
        if type(query) == str:
            preprocessed_query = self.topicModelGenerator.preprocess_text(query)
        elif isinstance(query, set):
            preprocessed_query = query

        # Classifies query to topic
        bow_vector = self.dictionary.doc2bow(preprocessed_query)
        queryTopics = self.lda_model[bow_vector]
        queryTopics = sorted(queryTopics, key=lambda x: (x[1]), reverse=True)

        #Returns -1 if probability of all topics are evenly distributed, ie unable to classify query
        min_dist = '%.3f' % (1/len(self.topicInvertedIndex))
        query_topic_dist = '%.3f' % queryTopics[0][1]
        if (min_dist == query_topic_dist):
            return -1

        # Returns topic with highest probabilty
        return queryTopics[0][0]

    def _get_topic_docs(self, topic):
        """Returns Documents of Topic from Inverted Index"""
        return self.topicInvertedIndex[str(topic)]

    def topic_score(self, topic, doc_id):
        """
        Calculates topic score of document
        Topic score is 1 + X/Y
        X = number of reviews that mention topic
        Y = Total review count
        X/Y is stored in topic inverted index
        """
        topic_docs = self._get_topic_docs(topic)

        topic_model_score = 1
        if doc_id in topic_docs:
            topic_model_score += topic_docs[doc_id]
        return topic_model_score
    