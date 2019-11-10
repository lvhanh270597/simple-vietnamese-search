

class Query:

    def __init__(self, query):
        self.query = query
    
    def transform(self, vectorizer):
        self.vector = vectorizer.transform([self.query])[0]
        return self.vector