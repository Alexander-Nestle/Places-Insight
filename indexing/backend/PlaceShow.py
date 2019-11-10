import json
from collections import defaultdict


class PlaceShow:
    """
    This module is in charge of how/what to display to user based on returned document key
    This would take search doc key as input.
    The output would be send to frontend for display, this module may also be directly invoked in frontend
    """
    def __init__(self, config):
        conf = config.conf
        self.data_doc = config.path + conf["data_file"]
        self.data_dict = defaultdict()

    def load(self):
        with open(self.data_doc, "rb") as f:
            data_doc_list = json.load(f)
            for doc in data_doc_list:
                self.data_dict[doc["place_id"]] = doc

    def get_item(self, key):
        doc = self.data_dict[key]
        return doc

    def show_text(self, key):
        doc = self.data_dict[key]
        output = ""
        cnt = 1
        for rev in doc["reviews"]:
            output += "Review " + str(cnt) + ": " + rev["text"].strip() + "\n"
            cnt += 1
        return output