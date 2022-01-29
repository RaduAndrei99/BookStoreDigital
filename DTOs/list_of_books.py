import json

class ListOfBooks(object):
    def __init__(self, books):
        self.books = books
        

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)