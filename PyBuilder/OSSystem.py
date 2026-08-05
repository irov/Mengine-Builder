import os
import subprocess


def _report(message):
    from PyBuilder.Error.ErrorHandler import ErrorHandler

    ErrorHandler.importantMessage(message)

class OSSystem(object):
    @staticmethod
    def system(commands):
        if isinstance(commands, (list, tuple)) is False:
            raise TypeError("OSSystem.system expects an argument list, not a shell command")

        result = subprocess.run(
            [os.fspath(command) for command in commands],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
        )

        if result.returncode != 0:
            _report("command: %s" % list(commands))
            _report("status: %s" % result.returncode)

            if result.stdout:
                _report("stdout: %s" % result.stdout.rstrip())

            if result.stderr:
                _report("stderr: %s" % result.stderr.rstrip())

            return False

        return True

    @staticmethod
    def tool(name, *arguments):
        from PyBuilder.Toolchain import ToolchainError, tool_path

        try:
            executable = tool_path(name)
        except ToolchainError as exception:
            _report(str(exception))
            return False

        return OSSystem.system([executable] + [os.fspath(argument) for argument in arguments])

    @staticmethod
    def process(commands):
        result = subprocess.run(
            [os.fspath(command) for command in commands],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
        )

        return result.returncode, result.stdout

    @staticmethod
    def process_tool(name, arguments):
        from PyBuilder.Toolchain import tool_path

        return OSSystem.process([tool_path(name)] + list(arguments))

    @staticmethod
    def run(commands, env=None):
        if isinstance(commands, (list, tuple)) is False:
            raise TypeError("OSSystem.run expects an argument list, not a shell command")

        process_environment = None

        if env is not None:
            process_environment = os.environ.copy()
            process_environment.update({str(key): os.fspath(value) for key, value in env.items()})

        result = subprocess.run(
            [os.fspath(command) for command in commands],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            env=process_environment,
        )

        return result.returncode == 0, result.stdout, result.stderr

    @staticmethod
    def run_tool(name, arguments):
        from PyBuilder.Toolchain import tool_path

        return OSSystem.run([tool_path(name)] + list(arguments))
    pass
