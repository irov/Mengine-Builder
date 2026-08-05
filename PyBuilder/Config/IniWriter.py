class IniWriter(object):
    def write(self,fp,data):
        self._prepareSection(fp,data)
        pass

    def _prepareSection(self,fp,data):
        for key,value in data.items():
            self._prepareOption(fp,key,value)
            pass
        pass

    def _prepareOption(self,fp,key,value):
        if isinstance(value,dict) is True:
            self._writeHeader(fp,key)
            self._prepareSection(fp,value)
            self._writeBuffer(fp,"\n")
            pass
        elif isinstance(value,list) is True:
            for val in value:
                self._writeOption(fp,key,val)
                pass
            pass
        else:
            self._writeOption(fp,key,value)
            pass
        pass

    def _writeBuffer(self,fp,data):
        fp.write(data)
        pass

    def _writeHeader(self,fp,headerName):
        data = "[%s]\n" % (headerName)
        self._writeBuffer(fp,data)
        pass

    def _writeOption(self,fp,key,val):
        data = "%s = %s\n" % (key,val)
        self._writeBuffer(fp,data)
        pass
    pass
