from config.config import config
from datetime import datetime
import os

class Log:
    
    def __init__(self, name="undefined"):
        self.name = name
        self.config = config["log"]
        path = self.config["log_path"]
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                print ("Successfully created the directory %s" % path)
        
        filename = self.config["log_name"] % ("%s.%s" % (self.name, self.config["log_ext"]))
        fullpath = os.path.join(path, filename)
        if not os.path.exists(fullpath):
            with open(fullpath, 'w'): pass
        self.fullpath = fullpath
        
    def write(self, content):
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        with open(self.fullpath, "a") as ofile:
            content = self.config["log_format"] % (dt_string, content)
            ofile.write("%s\n" % content)
            ofile.close()
    