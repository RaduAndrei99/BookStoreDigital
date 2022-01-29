import json

class BookDetails(object):
    def __init__(self, isbn, titlu, editura, an_publicare, gen_literar, pret):
        self.isbn = isbn
        self.titlu = titlu
        self.editura = editura
        self.an_publicare = an_publicare
        self.gen_literar = gen_literar
        self.pret = pret

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)