from Builder.Error.ErrorHandler import ErrorHandler
from Builder.OSSystem import OSSystem


def compile_python(source, destination):
    status, out, err = OSSystem.run_tool(
        "PythonCompiler", ["--in", source, "--out", destination]
    )

    if status is False:
        ErrorHandler.error(
            "[Compile] TinyPy compile file: %s out: %s error: %s" % (source, out, err)
        )

    return status
