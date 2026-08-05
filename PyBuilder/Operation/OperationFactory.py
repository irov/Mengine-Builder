from PyBuilder.Error.ErrorHandler import ErrorHandler

class OperationFactory:
    operationTypes = {}
    operationCache = {}

    @staticmethod
    def setProject(project):
        OperationFactory.project = project
        pass

    @staticmethod
    def registerOperationType(name, operationClassType):
        if OperationFactory.hasOperationType( name ):
            ErrorHandler.error("OperationFactory registerOperationType  already has %s" % name)
            pass

        OperationFactory.operationTypes[name] = operationClassType
        pass

    @staticmethod
    def hasOperationType(name):
        if name not in OperationFactory.operationTypes:
            return False
            pass

        return True
        pass

    @staticmethod
    def getCachedOperation(name):
        if name not in OperationFactory.operationCache:
            return None
            pass

        cachedOperation =  OperationFactory.operationCache[name]
        return cachedOperation
        pass

    @staticmethod
    def addCachedOperation(name, operation):
        OperationFactory.operationCache[name] = operation
        pass

    @staticmethod
    def createOperation(name):
        operationType = OperationFactory.operationTypes[name]
        operation = operationType()
        operation.setProject(OperationFactory.project)
        return operation
        pass

    @staticmethod
    def setAlias(aliasName, operationTypeName):
        operationType = OperationFactory.operationTypes[operationTypeName]
        OperationFactory.registerOperationType(aliasName,operationType)
        pass

    @staticmethod
    def getOperation(name, params):
        if OperationFactory.hasOperationType(name) is False:
            ErrorHandler.error("OperationFactory getOperation unknown operation %s" %name)
            return
            pass

        operation =  OperationFactory.getCachedOperation(name)
        if operation is None:
            operation = OperationFactory.createOperation(name)
            OperationFactory.addCachedOperation(name, operation)
            pass

        operation.onParams(params)
        return operation
        pass
    pass
