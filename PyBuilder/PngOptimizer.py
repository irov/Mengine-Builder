from PyBuilder.OSSystem import OSSystem
from PyBuilder.Environment import Environment
from PyBuilder.Error.ErrorHandler import ErrorHandler

import threading

class PngOptimizer(object):
    optimizedFiles = []
    portion = []

    limitCommandCount = 6500
    commandCount = 0

    @staticmethod
    def optimize(fileSourcePath, fileFullPath):
        if fileFullPath in PngOptimizer.optimizedFiles:
            return

        PngOptimizer.optimizedFiles.append(fileFullPath)
        PngOptimizer.portion.append([fileSourcePath,fileFullPath])
        pass

    @staticmethod
    def flush():
        if len(PngOptimizer.portion) == 0:
            return True
            pass

        failed = []

        thread_count = 8

        ts = []
        for n in range(thread_count):
            def __thread(portion, failed):
                for source, destination in portion:
                    project = Environment.getCurrentProject()

                    if project.imagePremultiply is True:
                        arguments = ("--in", source, "--out", destination, "--premultiply")
                    else:
                        arguments = ("--in", source, "--out", destination)
                        pass

                    if OSSystem.tool("AlphaSpreading", *arguments) is False:
                        failed.append(source)
                        pass
                    pass
                pass

            portion = PngOptimizer.portion[n::thread_count]

            t = threading.Thread(target=__thread, args=(portion, failed))
            t.start()
            ts.append(t)
            pass

        for t in ts:
            t.join()
            pass

        PngOptimizer.portion = []
        PngOptimizer.commandCount = 0

        if len(failed) != 0:
            for f in failed:
                ErrorHandler.warning("PngOptimizer failed: %s", f)
                pass

            return False
            pass

        return True
        pass

    @staticmethod
    def deleteOptimizedFiles():
        for filePath in PngOptimizer.optimizedFiles:
            #print("remove " + filePath)
            # FileSystem.removeFile(filePath)
            pass
        pass
    pass
