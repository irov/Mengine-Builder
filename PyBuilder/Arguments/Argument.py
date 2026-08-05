class Argument(object):
    def __init__(self, argName, description, important=True, default=None):
        self.description = description
        self.argName = argName
        self.value = None
        self.important = important
        self.default = default
        pass

    def getInfo(self):
        template = "%s - %s"
        info = template % (self.argName, self.description)

        argInfo = self._getInfo()
        if len(argInfo) > 0:
            info += ". " + argInfo
            pass

        return info
        pass

    def _getInfo(self):
        return ""
        pass

    def check(self, argName):
        if argName == self.argName:
            return True
            pass

        return False
        pass

    def setUpValue(self, inputValue):
        """returned True if set up was successful, else False"""
        if self.default is not None:
            self.value = self.default
            pass

        if inputValue is not None:
            if self._getData(self.argName, inputValue) is True:
                return True
                pass

            print("error in argument %s" % self.argName)
            return False
            pass

        if self.important is True and self.default is None:
            print("Can`t find argument %s" % self.argName)
            return False
            pass

        return True
        pass

    def _getData(self, argName, argValue):
        raise BaseException("Abstract must be derived")
        pass

    def getName(self):
        return self.argName
        pass

    def getValue(self):
        return self.value
        pass
    pass
