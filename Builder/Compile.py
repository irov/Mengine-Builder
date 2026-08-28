import sys
from pathlib import Path

from Builder.Error.ErrorHandler import ErrorHandler
from Builder.FileSystem import FileSystem

from Builder.OSSystem import OSSystem
from Builder.Toolchain import tool_path

def compile27(filename1):
    if sys.platform == "win32":
        commandLine = ['py', '-2', '-O', '-E', '-m', 'py_compile', filename1]
        environment = None
    else:
        executable = tool_path("python2.7")
        runtime_root = Path(executable).parent.parent
        commandLine = [executable, '-S', '-O', '-m', 'py_compile', filename1]
        environment = {
            "PYTHONHOME": str(runtime_root),
            "PYTHONPATH": "",
        }

    status, out, err = OSSystem.run(commandLine, env=environment)

    if status is False:
        ErrorHandler.error("[Compile] Python 2.7 compile file: %s out: %s error: %s"%(filename1, out, err))
        return status

    return status
