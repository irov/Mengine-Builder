from PyBuilder.TagHandler.ResourceHandler.ResourceHandler import ResourceHandler

class ResourceHandlerCursorSystem(ResourceHandler):
    def _onExecute(self):
        #We don`t need to parse children because child node File has path which equals to system cursor alias
        return True
        pass
    pass
