from PyBuilder.Error.ErrorHandler import ErrorHandler
from PyBuilder.Operation.OperationChain import OperationChain

class OperationManager(object):
    operationChains = list()

    @staticmethod
    def createOperationChain(**params):
        chain = OperationChain()
        chain.onParams(params)
        #OperationManager.operationChains.append(chain)
        return chain
        pass

    @staticmethod
    def runOperationChain(**params):
        params["AutoRun"] = True
        chain =  OperationManager.createOperationChain(**params)
        return chain
        pass

    @staticmethod
    def run():
        while True:
            chain = OperationManager.popNext()
            if chain is None:
                return
                pass

            if chain.run() is False:
                message = "Warning operation %s returned false. maybe it does not work correctly" % operation
                ErrorHandler.warning(message)
                return False
                pass
            pass

        return True

    @staticmethod
    def popNext():
        if len(OperationManager.operationChains) == 0:
            return None
            pass

        chain = OperationManager.operationChains.pop()
        return chain
        pass

    @staticmethod
    def printAllOperations():
        for chain in OperationManager.operationChains:
            print(chain)
            pass
        pass
    pass
