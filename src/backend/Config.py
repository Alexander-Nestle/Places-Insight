import json


class Config:
    """This manages the doc files used for different modules"""

    def __init__(self, path=""):
        self.path = path
        self.config_file = path + "config.json"
        with open(self.config_file, 'rb') as f:
            self.conf = json.load(f)
        self.data_file = path + self.conf["data_file"]
