import json
from collections import defaultdict

"""
This module is in charge of how/what to display to user based on returned document key
This would take search doc key as input.
The output would be send to frontend for display, this module may also be directly invoked in frontend 
"""
class PlaceShow:
    def __init__(self, refDocument):
        self.refDoc = refDocument
        self.refDict = defaultdict()

    def load(self):
        oriDocList = list()
        with open(self.refDoc, "rb") as f:
            oriDocList = json.load(f)
            for doc in oriDocList:
                self.refDict[doc["place_id"]] = doc

    def get_item(self, key):
        doc = self.refDict[key]
        return doc

    def show_text(self, key):
        doc = self.refDict[key]
        output = ""
        cnt = 1
        for rev in doc["reviews"]:
            output += "Review " + str(cnt) + ": " + rev["text"].strip() + "\n"
            cnt += 1
        return output


