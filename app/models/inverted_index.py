from system.data_structures.sentence import Sentence



class InvertedIndex:
    
    def __init__(self):
        self.terms = dict()
        self.docs = []
        self.sentence_instance = Sentence()

    def add_docs(self, docs):
        self.docs.extend(docs)
    
    def preprocess(self):
        for i, doc in enumerate(self.docs):
            self.sentence_instance.set_sentence(doc)
            self.sentence_instance.beautify()
            self.sentence_instance.tokenize(remove=False)
            doc = self.sentence_instance.remove()
            self.docs[i] = doc

    def calculate(self):
        for i, doc in enumerate(self.docs):
            words = doc.split()
            self._index(words, i)

    def _index(self, words, index):
        for word in words:
            if word not in self.terms:
                self.terms[word] = {index}
            else:
                self.terms[word].add(index)

    def fit(self):
        self.preprocess()
        self.calculate()

    def test(self):
        print(self.docs)
        print(self.terms)