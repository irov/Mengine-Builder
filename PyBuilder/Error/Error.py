class PyBuilderError (BaseException):
    def __init__(self,msg):
        self.msg = str(msg)
        super(PyBuilderError,self).__init__()
        pass

    def  __str__(self):
        return "PyBuilderError:" + self.msg
        pass
    pass
