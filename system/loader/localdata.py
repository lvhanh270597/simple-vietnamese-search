from config.config import config


class LocalData:
    
    def __init__(self):
        self.config = config["localdata"]
        self.load_data()

    def load_data(self):
        self.data = []
        self.data_path = self.config["data_path"]
        with open(self.data_path) as outfile:
            self.data = outfile.readlines()
        for i, _ in enumerate(self.data):
            self.data[i] = self.data[i].replace("\n", "")