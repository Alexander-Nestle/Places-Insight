class DocumentItem:
    """This class defines the structure of one touristic site"""
    def __init__(self, key, name, address, review_text):
        self.key = key
        self.name = name
        self.address = address
        self.review = review_text
        self.doc_len = 1

    def my_serialize(self):
        return self.review

    """Set document length, note this length are counted in words and have stop words removed"""
    def set_doclen(self, doc_len):
        self.doc_len = doc_len

class DocumentCollection:
    """This class defines the structure that serves for all documents"""
    def __init__(self):
        self.doc_num = 0
        self.avg_dl = 0

    """Add one document length here, and document number and average length will be changed accordingly"""
    def add_doc(self, doc_len):
        self.doc_num += 1
        if self.doc_num > 0:
            self.avg_dl = (self.avg_dl * (self.doc_num - 1) + doc_len)/self.doc_num