# ENV = dict()

config = dict()


config["database"] = {
    "host"  : "127.0.0.1",
    "port"  : "27017",
    "dbname": "visearch"
}

config["log"] = {
    "log_path"  : "/tmp/log",
    "log_name"  : "%s",
    "log_format": "%s: %s",
    "log_ext"   : "log"
}
