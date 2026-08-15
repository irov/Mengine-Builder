import json
import os
import platform
import sys
from pathlib import Path

from PyBuilder.ToolInstaller import ManifestError, ToolInstaller, ToolInstallerError


class ToolchainError(RuntimeError):
    pass


class UnsupportedPlatformError(ToolchainError):
    pass


class ToolNotFoundError(ToolchainError):
    pass


CONSOLE_ROOT = Path(__file__).resolve().parent.parent
_WINDOWS_ONLY_CONVERTERS = frozenset(("text2vso", "text2vso11", "text2pso", "text2pso11"))


def platform_name():
    if sys.platform == "win32":
        return "win32"

    if sys.platform == "darwin":
        machine = platform.machine().lower()

        if machine != "arm64":
            raise UnsupportedPlatformError(
                "Mengine-Builder supports macOS arm64 only (current architecture: %s)" % machine
            )

        return "macos"

    raise UnsupportedPlatformError("unsupported platform: %s" % sys.platform)


def platform_key():
    return "windows-x64" if platform_name() == "win32" else "macos-arm64"


def cache_root():
    return Path(os.environ.get("MENGINE_BUILDER_CACHE", CONSOLE_ROOT / ".cache")).resolve()


def platform_root():
    return cache_root() / "tools"


def _installer():
    return ToolInstaller(CONSOLE_ROOT, platform_key())


def tool_relative_path(name):
    try:
        return _installer().tool_relative_path(name)
    except ToolInstallerError as exception:
        if "unsupported" in str(exception):
            raise UnsupportedPlatformError(str(exception)) from exception

        raise ToolchainError(str(exception)) from exception


def tool_path(name, required=True):
    try:
        return str(_installer().resolve(name))
    except ToolInstallerError as exception:
        if required is False:
            return None

        message = str(exception)

        if "missing" in message:
            raise ToolNotFoundError(message) from exception

        if "unsupported" in message:
            raise UnsupportedPlatformError(message) from exception

        raise ToolchainError(message) from exception


def normalize_converter_params(params):
    normalized = {}

    for key, value in (params or {}).items():
        if key == "ffmpeg":
            value = tool_path("ffmpeg")

        normalized[str(key)] = str(value)

    return normalized


def converter_params_json(params):
    return json.dumps(normalize_converter_params(params), ensure_ascii=False, separators=(",", ":"))


def converter_supported(name):
    return platform_name() == "win32" or name not in _WINDOWS_ONLY_CONVERTERS


def required_tools_for_config(config):
    required = set()

    if config.get("python_compile", True) is True and platform_name() == "macos":
        required.add("python2.7")

    if config.get("metabuf") is True:
        required.add("Metawrite")

    if config.get("png_opt") is True:
        required.add("AlphaSpreading")

    image_mode = config.get("img_convert")

    if image_mode in ("convert_to_webp", "convert_to_webp_and_etc1"):
        required.update(("cwebp", "ImageTrimmer"))

    if image_mode in ("convert_to_etc1", "convert_to_webp_and_etc1"):
        required.add("ExtractorETC1")

    if image_mode == "convert_to_pvrtc":
        required.add("PVRTexToolCLI")

    if image_mode == "convert_to_dxt1":
        required.add("crunch")

    media_modes = (
        config.get("sound_convert"),
        config.get("music_convert"),
        config.get("video_convert"),
    )

    if any(value not in (None, False, "", "disable") for value in media_modes):
        required.update(("ffmpeg", "MengineConverter"))

    if config.get("no_exe") is not True and platform_name() == "win32":
        required.update(("ResourceHacker", "rc"))

    return sorted(required)


def check_tools(names):
    errors = []

    for name in names:
        try:
            tool_path(name)
        except ToolchainError as exception:
            errors.append(str(exception))

    return errors


def python_runtime_description():
    return "%s (%s)" % (sys.executable, platform.python_version())


def dependency_install_hint():
    if sys.platform == "darwin":
        return "brew install python-tk@3.14 pillow"

    return '"%s" -m pip install --user Pillow' % sys.executable
