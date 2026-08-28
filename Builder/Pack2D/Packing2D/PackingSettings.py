__author__ = 'human88998999877'

class PackingSettings(object):
    def __init__(self):
        super(PackingSettings, self).__init__()
        self.packingAlgorithm = None
        self.placeHeuristic = None
        self.sortOrder = None
        self.sortKey = None
        self.binSizeMode = None
        self.packingMode = None

        self.rotateMode = None
        self.maxWidth = None
        self.maxHeight = None
        self.border = None
        self.borderMode = None
        self.isDebug = False
        self.borderSize = None

        self.splitRule = None
        pass
    pass
