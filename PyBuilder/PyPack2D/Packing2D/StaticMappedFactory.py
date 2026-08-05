__author__ = 'human88998999877'
class StaticMappedFactoryError(BaseException):
    pass


class StaticMappedFactory(object):
    _types = {}
    _cache = {}

    @staticmethod
    def registerType(name, classType):
        if StaticMappedFactory.hasType( name ):
            raise StaticMappedFactoryError("TypeName already register %s" % name)
            pass

        StaticMappedFactory._types[name] = classType
        pass

    @staticmethod
    def hasType(name):
        if name not in StaticMappedFactory._types:
            return False
            pass

        return True
        pass

    @staticmethod
    def _getCachedInstance(name):
        if name not in StaticMappedFactory._cache:
            instance = StaticMappedFactory.createInstance(name)
            if instance is None:
                return None
                pass

            StaticMappedFactory._cache[name] = instance

            return instance
            pass

        instance =  StaticMappedFactory._cache[name]
        return instance
        pass

    @staticmethod
    def createInstance(name):
        instanceT = StaticMappedFactory._types[name]
        instance = instanceT()
        return instance
        pass

    @staticmethod
    def getInstance(name, cached = True):
        if StaticMappedFactory.hasType(name) is False:
            raise StaticMappedFactoryError("TypeName not register %s" % name)
            pass

        instance = None

        if cached is True:
            instance = StaticMappedFactory._getCachedInstance()
            pass
        else:
            instance = StaticMappedFactory._getInstance()
            pass

        return instance
        pass
    pass
