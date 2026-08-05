import os

class Environment:
    CURRENT_PROJECT = None

    @staticmethod
    def getCurrentProject():
        return Environment.CURRENT_PROJECT
        pass

    @staticmethod
    def setCurrentProject(project):
        Environment.CURRENT_PROJECT = project
        pass

    @staticmethod
    def printSystemEnviron():
        env = str(os.environ)
        envArr = env.split(",")
        for envPart in envArr:
            print (envPart)
            pass
        pass
    pass
#printEnvironment()
