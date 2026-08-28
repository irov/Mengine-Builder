from Builder.Logger import Logger
from Builder.Error.ErrorHandler import ErrorHandler
from Builder.Environment import Environment
from Builder.Error.ErrorListener import ErrorListener
from Builder.FileSystem import FileSystem
from Builder.Watcher.Watcher import Watcher

class Builder:
    def __init__(self):
        self.errorListener = ErrorListener()
        self.project = None
        self.actions = []
        self.logger = None
        pass

    def initErrorHandler(self, errorReporting):
        ErrorHandler.addListener(self.errorListener)
        ErrorHandler.setErrorReporting(errorReporting)
        pass

    def addAction(self,action):
        self.actions.append(action)
        pass

    def prepare(self,project):
        if not FileSystem.isFile(project.pathToApplicationJson):
            ErrorHandler.error("Application JSON not exist %s" % project.pathToApplicationJson)
            return False
            pass

        if not FileSystem.isFile(project.pathToProtocolXml):
            ErrorHandler.error("protocol.xml not exist %s" % project.pathToProtocolXml)
            return False
            pass

        if not FileSystem.isDirectory(project.pathToSourceExe) and project.NoExe is False:
            ErrorHandler.error("directory with execution files not exist %s" % project.pathToSourceExe)
            return False
            pass

        # if not FileSystem.isDirectory(project.pathToResources):
        #     ErrorHandler.error("directory with game resources not exist %s" % project.pathToResources)
        #     return False
        #     pass

        if not FileSystem.isDirectory(project.destinationDir):
            ErrorHandler.importantMessage("making directory %s" % project.destinationDir)
            FileSystem.makeDirsRecursive(project.destinationDir)
            pass

        elif FileSystem.isEmptyDir( project.destinationDir ) is False and project.removeDestDirIfExist is False:
            ErrorHandler.importantMessage("warning directory %s not empty" % project.destinationDir)
            pass

        elif project.removeDestDirIfExist is True:
            pathlogs = self.logger.getPathToLogs()
            self.logger.finalise()

            FileSystem.removeDirRecursive(project.destinationDir)
            FileSystem.makeDirsRecursive(project.destinationDir)

            print("!!!!!!!!!!!!!!!!!!!!Remove Dir", project.logDir)
            FileSystem.removeDirRecursive(project.logDir)
            FileSystem.makeDirsRecursiveIfNotExist(project.logDir)
            # FileSystem.makeDirsRecursive(project.logDir)

            self.logger.initialise(pathlogs)
            pass

        if not FileSystem.isDirectory(project.pathToDestinationExe):
            ErrorHandler.importantMessage("making directory %s" % project.pathToDestinationExe)
            FileSystem.makeDirsRecursive(project.pathToDestinationExe)
            pass

        return True
        pass

    def initialise(self, project):
        if self.prepare(project) is False:
            ErrorHandler.warning("invalid prepare project")
            return False
            pass

        Environment.setCurrentProject(project)

        for action in self.actions:
            if action.initialise(self, project) is False:
                ErrorHandler.error("Initialise build action error %s" % action)
                return False
                pass
            pass

        self.project = project

        return True
        pass

    def finalise(self):
        ErrorHandler.importantMessage("Finalise build")

        for action in self.actions:
            if action.finalise() is False:
                ErrorHandler.error("Finalise build action error %s" % action)
                return False
                pass
            pass

        ErrorHandler.removeListener(self.errorListener)

        return True
        pass

    def createLogger(self, logDir):
        if FileSystem.isDirectory(logDir) is False:
            FileSystem.makeDirsRecursive(logDir)
            pass

        self.logger = Logger()
        self.logger.initialise(logDir)

        ErrorHandler.importantMessage("Log created  %s"%self.logger.getFileName())

        self.errorListener.setLogger(self.logger)
        pass

    def buildActions(self):
        for action in self.actions:
            ErrorHandler.importantMessage("Running action %s" % action)
            if action.run() is False:
                ErrorHandler.error("Build action error %s" % action)
                return False
                pass
            pass

        return True
        pass

    def build(self):
        ErrorHandler.importantMessage("Build in %s" % self.project.destinationDir)

        Watcher.startInterval("BUILD")
        result = self.buildActions()
        Watcher.stopInterval("BUILD")

        return result
        pass
    pass
