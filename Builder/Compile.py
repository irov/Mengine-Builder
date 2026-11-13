from Builder.Error.ErrorHandler import ErrorHandler
from Builder.OSSystem import OSSystem


def _run_python_compiler(arguments):
    status, out, err = OSSystem.run_tool("PythonCompiler", arguments)

    if status is False:
        ErrorHandler.error(
            "[PythonCompiler] arguments: %s\nstdout: %s\nstderr: %s",
            arguments, out, err,
        )

    return status


def compile_python(source, destination):
    return _run_python_compiler(["--in", source, "--out", destination, "-D_DEVELOPMENT=False"])


def validate_python(source):
    return _run_python_compiler(["--in", source, "--validate"])
