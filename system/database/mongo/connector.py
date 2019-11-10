import pymongo
from config.config import config

class AccessDatabase:

    def __init__(self):
        self.config = config["database"]
        self.accessor = pymongo.MongoClient("mongodb://%s:%s/" % (self.config["host"], self.config["port"]))
        self.mydb = self.accessor[self.config["dbname"]]

    def write(self, colName, data):
        print("Size of data: %d" % len(data))
        mycol = self.mydb[colName]
        items = mycol.insert_many(data).inserted_ids
        print("Wrote %d/%d successfully!" % (len(items), len(data)))

    def find_one(self, colName, condition={}, fields=None):
        mycol = self.mydb[colName]
        data = mycol.find_one(condition, fields)
        return data

    def find(self, colName, condition={}, fields=None):
        mycol = self.mydb[colName]
        data = mycol.find(condition, fields)
        return data

    def test(self, colName):
        for item in self.find(colName):
            print(item)
