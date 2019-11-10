from system.data_structures.sentence import Sentence

class Document:

    def __init__(self, loader, colName, fields):
        self.docs = []
        self.loader = loader
        self.colName = colName
        self.fields = fields
        self.sentence_instance = Sentence()

    def load_data(self, colName):
        db_data = self.loader.db.find(colName, {})
        self.docs = []
        for item in db_data:
            self.docs.append(item)
       
    def preprocess(self):
        for i, doc in enumerate(self.docs):
            for field in self.fields:
                data_field = doc[field]
                self.sentence_instance.set_sentence(data_field)
                self.sentence_instance.beautify()
                self.sentence_instance.tokenize(remove=False)
                data_field = self.sentence_instance.remove()
                doc[field] = data_field
            self.docs[i] = doc

    def fit(self):
        self.load_data(self.colName)
        self.preprocess()
