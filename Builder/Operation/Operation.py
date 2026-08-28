from Builder.Error.ErrorHandler import ErrorHandler

from Builder.Watcher.Watcher import Watcher

class Operation(object):
    def __init__(self):
        super(Operation, self).__init__()

        self._success = False
        self.project = None
        pass

    def setProject(self, project):
        self.project = project
        pass

    def onParams(self, params):
        self.name = params.pop("Name", None)
        self._onParams(params)
        pass

    def run(self):
        interval_name = "Operation [{}]".format(self.__class__.__name__)
        Watcher.startInterval(interval_name)

        try:
            self._success = self._onRun()
        finally:
            Watcher.stopInterval(interval_name)

        return self._success
        pass

    def _onRun(self):
        raise BaseException("Abstract Must Be Derived")
        pass

    def _onParams(self, params):
        pass

    def isSuccess(self):
        return self._success
        pass

    def getInfo(self):
        info = self._getInfo()
        return "<%s> :: %s" % (self.__class__.__name__, info)
        pass

    def _getInfo(self):
        return ""
        pass

    def __repr__(self):
        return self.getInfo()
        pass
    pass
