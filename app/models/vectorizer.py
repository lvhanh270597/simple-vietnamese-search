from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

class Vectorizer:

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.pca = PCA()

    def set_docs(self, docs):
        self.docs = docs

    def fit_transform(self):
        self.output = self.vectorizer.fit_transform(self.docs)
        self.output = self.pca.fit_transform(self.output.toarray())
        self.output = self.output.astype("float32")
        return self.output

    def transform(self, docs):
        results = self.vectorizer.transform(docs)
        results = self.pca.transform(results.toarray())
        results = results.astype("float32")
        return results
