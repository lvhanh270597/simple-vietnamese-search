from config.config import config
from system.database.mongo import connector
from system.logs.log import Log

class Loader:

    def __init__(self, list_load=None):
        self.log = Log("main-loader")
        self.load_database()

    def load_database(self):
        try:
            self.db = connector.AccessDatabase()
        except:
            self.log.write("Can't connect to the database!")
