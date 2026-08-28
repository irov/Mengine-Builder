__author__ = 'human88998999877'

from Builder.Watcher.Watcher import Watcher

class BuilderAction(object):
    def __init__(self):
        super(BuilderAction,self).__init__()
        pass

    def __str__(self):
        return "<%s>" % self.__class__.__name__
        pass

    def __repr__(self):
        return self.__str__()
        pass

    def initialise(self, builder, project):
        self.builder = builder
        self.project = project
        return self._onInitialise()
        pass

    def run(self):
        interval_name = "Action [{}]".format(self.__class__.__name__)
        Watcher.startInterval(interval_name)

        try:
            result = self._onRun()
        finally:
            Watcher.stopInterval(interval_name)

        return result
        pass

    def finalise(self):
        return self._onFinalise()
        pass

    def _onInitialise(self):
        return True
        pass

    def _onRun(self):
        return True
        pass

    def _onFinalise(self):
        return True
        pass
    pass
