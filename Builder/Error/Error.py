class BuilderError (BaseException):
    def __init__(self,msg):
        self.msg = str(msg)
        super(BuilderError,self).__init__()
        pass

    def  __str__(self):
        return "BuilderError:" + self.msg
        pass
    pass
