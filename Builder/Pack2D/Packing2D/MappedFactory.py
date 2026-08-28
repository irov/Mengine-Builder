__author__ = 'human88998999877'
class MappedFactoryError(BaseException):
    pass

class MappedFactory(object):
    def __init__(self):
        super(MappedFactory, self).__init__()
        self._types = {}
        #self._cache = {}
        pass

    def register(self, name, classType):
        if self.hasType( name ):
            raise MappedFactoryError("TypeName already register %s" % name)
            pass

        self._types[name] = classType
        pass

    def hasType(self, name):
        if name not in self._types:
            return False
            pass

        return True
        pass

#    def _getCachedInstance(self, name):
#        if name not in self._cache:
#            instance = self.createInstance(name)
#            if instance is None:
#                return None
#                pass
#
#            self._cache[name] = instance
#
#            return instance
#            pass
#
#        instance =  self._cache[name]
#        return instance
#        pass

    def __createInstance(self, name):
        instanceT = self._types[name]
        instance = instanceT()
        return instance
        pass

    def getInstance(self, name):
        if self.hasType(name) is False:
            raise MappedFactoryError("TypeName not register %s" % name)
            return None
            pass

        instance = self.__createInstance(name)
        return instance
        pass
    pass
