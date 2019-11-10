from flask import Flask, request, render_template, redirect, url_for
from backend.PlaceSearch import PlaceSearch, PlaceShow
from backend.FileManager import FileManager
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query_str = request.form.get('searchbox')
        #print("Query string is " + str(queryStr))
        doc_list = plc_search.search(query_str)
        result_list = [plc_show.get_item(doc_item[0]) for doc_item in doc_list[0:max_display]]
        return render_template('result.html', querystr=query_str, resultlist=result_list, resultlen=len(result_list))
        #return "query string is " + str(queryStr)
    return render_template('index.html')

if __name__ == '__main__':
    """First we do initilization"""
    print(os.getcwd())
    fmanager = FileManager()
    dir_prefix = "./backend/"
    data_file = dir_prefix + fmanager.data_file
    index_file = dir_prefix + fmanager.index_file
    doc_file = dir_prefix + fmanager.doc_file
    plc_search = PlaceSearch(index_file, doc_file)
    plc_search.load()
    plc_show = PlaceShow(data_file)
    plc_show.load()
    max_display = 20

    app.run(debug=True, port=5000)