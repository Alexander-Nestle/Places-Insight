import json

class JsonIO:
    """Class Performs JSON IO"""
    @staticmethod
    def read_json_file(path) -> []:
        """Reads in JSON File"""
        with open(path) as f:
            return json.load(f)

    @staticmethod
    def write_json_file(path, data):
        """Writes Data JSON File Using Dump"""
        with open(path, 'w') as json_file:
            d = json.dumps(data)
            json_file.write(d)

    @staticmethod
    def write_lst(lst,file_):
        """Writes List to JSON File with '\n Delimiter'"""
        try:
            iterator = iter(lst)
        except TypeError:
            return
        else:
            with open(file_,'w') as f:
                for l in iterator:
                    f.write(" ".join(l))
                    f.write('\n')

    @staticmethod
    def read_lst(file):
        """Reads List from JSON file with \n Delimiter"""
        return [line.rstrip('\n').split() for line in open(file)]
