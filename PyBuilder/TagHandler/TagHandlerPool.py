class TagHandlerPool:
    def __init__(self, project):
        self.project = project
        self.handlers = {}
        self.tags = []
        self.imageQuality = None
        self.soundQuality = None
        pass

    def setResourceTags(self, tags):
        self.tags = [] if len(tags) == 0 else tags.split(' ')
        pass

    def setImageQuality(self, imageQuality):
        self.imageQuality = imageQuality
        pass

    def setSoundQuality(self, soundQuality):
        self.soundQuality = soundQuality
        pass

    def removeResourceTags(self):
        self.tags = []
        pass

    def getTags(self):
        return self.tags
        pass

    def setHandler(self, name, handler):
        handler.setProject(self.project)

        self.handlers[name] = handler
        pass

    def getHandler(self, name):
        if name not in self.handlers:
            return None
            pass

        handler = self.handlers[name]
        return handler
        pass
    pass
