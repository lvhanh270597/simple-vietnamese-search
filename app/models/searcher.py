from app.models.vectorizer import Vectorizer
from app.models.querier import Query
import numpy as np
import operator
import faiss

class Searcher:

    def __init__(self, document, fields, number_results=10):
        self.number_results = number_results
        self.document = document
        self.set_fields(fields)
        self.document.fit()
    
    def set_fields(self, fields):
        self.fields = fields

    def set_docs(self, docs):
        self.docs = docs
        self.indexed_docs = dict()
        for field in self.fields["index"]:
            data_field = []
            for doc in docs:
                data_field.append(doc[field])
            self.indexed_docs[field] = data_field

    def fit(self):
        self.set_docs(self.document.docs)
        self.vectorizers = dict()
        self.dims = dict()
        for field in self.fields["index"]:
            data = self.indexed_docs[field]
            vectorizer = Vectorizer()
            vectorizer.set_docs(data)
            data = vectorizer.fit_transform()
            data = np.ascontiguousarray(data)
            self.indexed_docs[field] = data
            self.vectorizers[field] = vectorizer
            self.dims[field] = self.indexed_docs[field].shape[1]
    
        self.faiss_indices = dict()
        for field in self.fields["index"]:
            self.faiss_indices[field] = faiss.IndexFlatL2(self.dims[field])
            self.faiss_indices[field] = self.faiss_indices[field].add(self.indexed_docs[field])

    def search(self, query):
        self.score = dict()
        for field in self.fields["index"]:
            vector = Query(query).transform(self.vectorizers[field])
            matrix = np.array([vector])
            D, I = self.faiss_indices[field].search(matrix, self.number_results)
            D, I = D[0], I[0]
            for i in I:
                if i not in self.score:
                    self.score[i] = D
                else:
                    self.score[i] = min(self.score[i], D)
        self.show()
    
    def show(self):
        scores = sorted(self.score.items(), key=operator.itemgetter(1))
        for key, _ in scores:
            for field in self.fields["show"]:
                print(self.docs[field])
            print("#" * 50)

