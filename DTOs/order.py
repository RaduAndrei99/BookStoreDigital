import json
from datetime import datetime
class Order(object):
    def __init__(self, items, status):
        self.data = str(datetime.now())
        self.items = items
        self.status = status

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)