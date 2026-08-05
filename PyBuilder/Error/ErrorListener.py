__author__ = 'human88998999877'

from PyBuilder.Error.Error import PyBuilderError
import os

class ErrorListener(object):
    def __init__(self):
        self.logger = None
        pass

    def setLogger(self, logger):
        self.logger = logger
        pass

    def onError(self, error):
        message = error.getMessage()

        print(message)

        if error.isLogged is True and self.logger is not None:
            self.logger.write(message)
            pass
        pass
    pass
