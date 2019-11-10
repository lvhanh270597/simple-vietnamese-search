from app.models.document import Document
from system.loader.loader import Loader
from app.models.searcher import Searcher

class Main:
    
    def __init__(self):
        loader = Loader()
        document = Document(loader, "post", ["title", "content"])
        
        fields = {
            "index" : ["title", "content"],
            "show"  : ["_id", "title"]
        }
        searcher = Searcher(document, fields)
        searcher.fit()
        while True:
            query = input("Enter your query: ")
            searcher.search(query)

Main()