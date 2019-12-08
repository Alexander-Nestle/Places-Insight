from flask import Flask, request, render_template, redirect, url_for
from backend.PlaceSearch import SearchRank, PlaceShow
from backend.Config import Config
from backend.DataBase import DBManager
from backend.topicModel.TopicModelService import TopicModelService
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query_str = request.form.get('searchbox')
        doc_list = plc_search.search(query_str)
        result_list = [topic_model_service.map_topic_string(plc_show.get_item(doc_item[0])) for doc_item in doc_list[0:max_display]]
        return render_template('result.html', querystr=query_str, resultlist=result_list, resultlen=len(result_list))
    return render_template('index.html')


if __name__ == '__main__':
    """First we do initialization"""
    print(os.getcwd())
    dir_prefix = "./backend/"
    db_config = Config(dir_prefix)
    DBManager.initialize(db_config)
    DBManager.set_path(dir_prefix)

    plc_search = SearchRank(db_config)
    plc_search.initialize()
    plc_show = PlaceShow(db_config)
    plc_show.load()
    topic_model_service = TopicModelService('./backend/topicModel/model/model', './backend/topicModel/preprocessed_reviews.txt', './backend/topicModel/topicInvertedIndex.json')
    max_display = 20

    app.run(debug=True, port=5000)