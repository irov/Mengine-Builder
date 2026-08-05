from PyBuilder.Error.ErrorHandler import ErrorHandler

import time

class TimeInterval(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.timeStart = 0.0
        self.timeLength = 0.0
        pass

    def start(self):
        self.timeStart = time.time()
        pass

    def stop(self):
        timeEnd = time.time()

        self.timeLength += timeEnd - self.timeStart
        pass

    def length(self):
        return self.timeLength
        pass

    def tabs(self):
        if self.parent is None:
            return 0

        return 1 + self.parent.tabs()
        pass

    def top(self):
        if self.parent is None:
            return self

        return self.parent.top()
        pass

    def percent(self):
        if self.parent is None:
            return 100
            pass

        top = self.top()

        parent_length = top.length()

        if parent_length <= 0.00001:
            return 100

        return int(self.length() / parent_length * 100.0)
        pass
    pass


class Watcher(object):
    timeIntervals = []
    stackIntervals = []

    @staticmethod
    def getTimeIntervals(name, parent):
        for interval in Watcher.timeIntervals:
            if interval.name != name or interval.parent != parent:
                continue

            return interval
            pass

        interval = TimeInterval(name, parent)

        Watcher.timeIntervals.append(interval)

        return interval
        pass

    @staticmethod
    def startInterval(name):
        if len(Watcher.stackIntervals) == 0:
            parent = None
        else:
            parent = Watcher.stackIntervals[-1]
            pass

        interval = Watcher.getTimeIntervals(name, parent)
        interval.start()

        Watcher.stackIntervals.append(interval)
        pass

    @staticmethod
    def stopInterval(name):
        interval = Watcher.stackIntervals.pop(-1)

        if interval.name != name:
            raise RuntimeError("Watcher [{}] pop [{}]".format(name, interval.name))
            pass

        interval.stop()

        delta = interval.length()

        return delta
        pass

    @staticmethod
    def printTotal():
        print("=======================================")
        print("Watcher:")
        for interval in Watcher.timeIntervals:
            print("{}Interval: {} {} ({}%)".format(" " * interval.tabs(), interval.name, interval.length(), interval.percent()))
            pass
        print("=======================================")
    pass
