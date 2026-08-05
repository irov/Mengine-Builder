#!/usr/bin/env python3

import platform
import sys
import traceback


MINIMUM_PYTHON = (3, 11)


def _dependency_hint():
    if sys.platform == "darwin":
        return "brew install python-tk@3.14 pillow"

    if sys.platform == "win32":
        return '"%s" -m pip install --user Pillow' % sys.executable

    return '"%s" -m pip install --user Pillow' % sys.executable


def _check_runtime():
    print("ProjectBuilder Python: %s (%s)" % (sys.executable, platform.python_version()))

    if sys.version_info < MINIMUM_PYTHON:
        print(
            "ProjectBuilder requires Python %d.%d or newer. Install/activate a compatible Python."
            % MINIMUM_PYTHON,
            file=sys.stderr,
        )

        if sys.platform == "darwin":
            print("Install it with: brew install python@3.14 pillow", file=sys.stderr)
            print("Then run: /opt/homebrew/bin/python3.14 ProjectBuilder.py ...", file=sys.stderr)

        return False

    try:
        import PIL
    except ImportError:
        print("ProjectBuilder requires Pillow. Install it with: %s" % _dependency_hint(), file=sys.stderr)
        return False

    print("Pillow: %s" % getattr(PIL, "__version__", "unknown"))
    return True


def _argument_value(arguments, name):
    try:
        return arguments[arguments.index(name) + 1]
    except (ValueError, IndexError):
        return None


def _load_preflight_config(arguments):
    from PyBuilder.ConfigLoader import load_build_config

    path = _argument_value(arguments, "-path_config")

    if path is None:
        return None

    return load_build_config(path, arguments)


def _preflight(arguments):
    from PyBuilder.Toolchain import (
        ToolchainError,
        check_tools,
        platform_name,
        platform_root,
        required_tools_for_config,
    )

    try:
        selected_platform = platform_name()
    except ToolchainError as exception:
        print(str(exception), file=sys.stderr)
        return False

    print("Mengine-Builder platform: %s (%s)" % (selected_platform, platform_root()))

    config = _load_preflight_config(arguments)

    if config is None:
        return True

    errors = check_tools(required_tools_for_config(config))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)

        return False

    return True


def main(arguments=None):
    arguments = list(sys.argv[1:] if arguments is None else arguments)

    if "run" in arguments[:2]:
        print("The legacy 'run run' prefix is no longer supported.", file=sys.stderr)
        return 2

    if _check_runtime() is False:
        return 2

    if "--help" in arguments:
        arguments[arguments.index("--help")] = "-help"

    help_requested = arguments == ["-help"]

    if help_requested is False:
        try:
            if _preflight(arguments) is False:
                return 2
        except (OSError, ValueError) as exception:
            print("ProjectBuilder preflight failed: %s" % exception, file=sys.stderr)
            return 2

    try:
        from PyBuilder.PyBuilderConsoleApp import PyBuilderConsoleApp

        application = PyBuilderConsoleApp()
        application.initialise()
        result = application.run(*arguments)
        return 0 if result is True or help_requested is True else 1
    except Exception:
        traceback.print_exc(file=getattr(sys, "__stderr__", sys.stderr))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
