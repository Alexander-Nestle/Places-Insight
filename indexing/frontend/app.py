from flask import Flask, request, render_template, redirect, url_for
from indexing.backend.PlaceSearch import PlaceSearch
from indexing.backend.PlaceShow import PlaceShow

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        queryStr = request.form.get('searchbox')
        #print("Query string is " + str(queryStr))
        doclist = plcSearch.search(queryStr)
        resultlist = [plcShow.get_item(docItem[0]) for docItem in doclist[0:maxDisplay]]
        return render_template('result.html', querystr=queryStr, resultlist=resultlist, resultlen=len(resultlist))
        #return "query string is " + str(queryStr)
    return render_template('index.html')

if __name__ == '__main__':
    """First we do initilization"""
    oriDocFile = "../backend/dataset.json"
    indexFile = "../backend/dataindex.json"
    docFile = "../backend/datadoc.json"
    plcSearch = PlaceSearch(indexFile, docFile)
    plcSearch.load()
    plcShow = PlaceShow(oriDocFile)
    plcShow.load()
    maxDisplay = 20

    app.run(debug=True, port=5000)