import os

from yaml import safe_load

class Config:
    def __init__(self, conf: str = None):
        self._conf = conf
        self._datadir = None
        self._network = None

        try:
            if conf:
                if not os.path.exists(conf):
                    raise FileNotFoundError("Error: config.yml is missing")
                
                with open(conf, "r") as file:
                    cfile = safe_load(file)
                    self._datadir = cfile.get("datadir")
                    self._network = cfile.get("network")
        except Exception as e:
            print(e)

    @property
    def datadir(self):
        return self._datadir
    
    @property
    def network(self):
        return self._network
