from indexing.backend.PlaceSearch import PlaceSearch
from indexing.backend.PlaceShow import PlaceShow

query_str = "child friendly restaurant"
max_shown = 8
show_counter = 0
oriDocFile = "PlacesResults.json"
indexFile = "PlacesIndex.json"
docFile = "PlacesDoc.json"

"""First, build a search object"""
plcSearch = PlaceSearch(indexFile, docFile)
plcSearch.load()

plcShow = PlaceShow(oriDocFile)
plcShow.load()

query_doc_list = plcSearch.search(query_str, max_shown)
for query_item in query_doc_list:
    query_doc_item = query_item[0]
    print("=" * 20 + " Result " + str(show_counter) + " " + "="*20)
    print("BM25 score: " + str(query_item[1]))
    print("Document Key: " + str(query_item[0]))
    """
    print("name: " + query_doc_item.name)
    print("address: " + query_doc_item.address)
    print("review: " + query_doc_item.review)
    """
    print(plcShow.show(str(query_item[0])))
    show_counter += 1