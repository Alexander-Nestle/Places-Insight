import json
from backend.ReviewDocument import DocumentItem, DocumentCollection

"""parse the review documents into documentItems"""
class JsonParser:
    def __init__(self, filename):
        self.filename = filename
        self.doc_list = []
        self.doc_idx = 0

    def parse(self):
        with open(self.filename, 'rb') as f:
            self.doc_list = json.load(f)

    def has_more_item(self):
        return self.doc_idx < len(self.doc_list)

    def get_next_item(self):
        if len(self.doc_list) == 0:
            print("Error: need to parse before getitem")
            return
        if self.doc_idx >= len(self.doc_list):
            print("Error: index has exceeded maximum item numbers")
            return
        item_raw = self.doc_list[self.doc_idx]
        item_key = item_raw['place_id']
        item_name = item_raw['name']
        item_address = item_raw['formatted_address']
        item_text = ""
        for item_rev in item_raw['reviews']:
            if "language" in item_rev.keys() and item_rev["language"].lower() != "en":
                continue
            item_text += item_rev["text"]
            item_text += " "
            # I guess we could add some filter here for the "time" attribute

        self.doc_idx += 1
        return DocumentItem(item_key, item_name, item_address, item_text)