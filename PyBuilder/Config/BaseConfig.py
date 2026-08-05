class BaseConfig(object):
    def __init__(self):
        super(BaseConfig,self).__init__()
        self.data = {}
        pass

    def getDict(self):
        return self.data
        pass

    def read(self,pathTo):
        self.data = {}
        self._read(pathTo)
        pass

    def write(self,path):
        with open(path, "w") as fp:
            self._write(fp)
            pass
        pass

    def __delitem__(self, key):
        del self.data[key]
        pass

    def __getitem__(self, item):
        return self.data[item]
        pass

    def __setitem__(self, item, val):
        self.data[item] = val
        pass

    def __iter__(self):
        return self.data.__iter__()
        pass

    def items(self):
        return self.data.items()
        pass

    def __repr__(self):
        return "%s < %s >" % (self.__class__.__name__, str(self.data))
        pass
    pass
