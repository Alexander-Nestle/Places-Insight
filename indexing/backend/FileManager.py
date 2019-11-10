class FileManager:
    """This manages the doc files used for different modules"""

    def __init__(self):
        self.data_file = "dataset.json"
        self.index_file = "dataindex.json"
        self.doc_file = "datadoc.json"

    def set_files(self, data_file, index_file, doc_file):
        self.data_file = data_file
        self.index_file = index_file
        self.doc_file = doc_file
