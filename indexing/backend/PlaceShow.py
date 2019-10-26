import json
from collections import defaultdict

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

    def show(self, key):
        doc = self.refDict[key]
        output = ""
        cnt = 1
        for rev in doc["reviews"]:
            output += "Review " + str(cnt) + ": " + rev["text"].strip() + "\n"
            cnt += 1
        return output


