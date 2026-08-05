"""Pure Python compatibility facade for the former C++ ToolsBuilderPlugin."""

import hashlib
import json
import os
import sys
import tempfile

from PIL import Image as PillowImage
from PIL import ImageChops

from PyBuilder.OSSystem import OSSystem
from PyBuilder.Toolchain import converter_params_json, tool_path


def _absolute(path):
    return os.path.abspath(os.fspath(path))


def _run_native(name, arguments):
    success, stdout, stderr = OSSystem.run_tool(name, arguments)

    if success is False:
        message = stderr.strip() or stdout.strip() or "unknown error"
        raise RuntimeError("%s failed: %s" % (name, message))

    return True


def writeBin(protocol_path, xml_path, bin_path):
    return _run_native(
        "Metawrite",
        ("--protocol", _absolute(protocol_path), "--in", _absolute(xml_path), "--out", _absolute(bin_path)),
    )


def convert(from_path, to_path, convert_type, params):
    if convert_type == "ffmpegToGVF":
        raise RuntimeError("ffmpegToGVF is not registered in the legacy ProjectBuilder")

    return _run_native(
        "MengineConverter",
        (
            "--converter",
            str(convert_type),
            "--in",
            _absolute(from_path),
            "--out",
            _absolute(to_path),
            "--params-json",
            converter_params_json(params),
        ),
    )


def isAlphaInImageFile(path):
    with PillowImage.open(path) as image:
        return "A" in image.getbands() or "transparency" in image.info


def _has_useful_alpha(image):
    if "A" not in image.getbands() and "transparency" not in image.info:
        return False

    alpha = image.convert("RGBA").getchannel("A")
    return ImageChops.difference(alpha, PillowImage.new("L", image.size, 255)).getbbox() is not None


def isUselessAlphaInImageFile(path):
    with PillowImage.open(path) as image:
        return _has_useful_alpha(image) is False


def isPow2SquadImageFile(path):
    with PillowImage.open(path) as image:
        width, height = image.size

    return width == height and width > 0 and (width & (width - 1)) == 0


def _normalize_image(image):
    image.load()

    if image.mode in ("1", "P", "LA", "CMYK"):
        return image.convert("RGBA")

    if image.mode not in ("L", "RGB", "RGBA"):
        return image.convert("RGBA")

    return image


def loadImage(path):
    with PillowImage.open(path) as source:
        return _normalize_image(source).copy()


def saveImage(image, path):
    try:
        image.save(path)
    except (OSError, ValueError):
        return False

    return True


def _byte_component(value):
    value = float(value)

    if 0.0 <= value <= 1.0:
        value *= 255.0

    return max(0, min(255, int(round(value))))


def createImage(width, height, channels, color):
    modes = {1: "L", 3: "RGB", 4: "RGBA"}

    if channels not in modes:
        raise ValueError("unsupported image channel count: %s" % channels)

    components = tuple(_byte_component(component) for component in color[:channels])
    fill = components[0] if channels == 1 else components
    return PillowImage.new(modes[channels], (int(width), int(height)), fill)


def getImageWidth(image):
    return image.width


def getImageHeight(image):
    return image.height


def getImageChannels(image):
    return len(image.getbands())


def pasteImage(image, paste_image, x, y):
    try:
        image.paste(paste_image, (int(x), int(y)))
    except (ValueError, TypeError):
        return False

    return True


def putImageData(image, data):
    image.putdata([tuple(pixel) if len(pixel) > 1 else pixel[0] for pixel in data])
    return True


def rotateImage(image, angle):
    return image.rotate(float(angle), expand=True)


def getImageExtremColor(image):
    extrema = image.getextrema()
    return [extrema] if isinstance(extrema[0], int) else list(extrema)


def uselessalphaImage(image):
    return _has_useful_alpha(image) is False


def splitImage(image):
    rgba = image.convert("RGBA")
    return rgba.convert("RGB"), rgba.getchannel("A")


def releaseImage(image):
    image.close()


def getImageData(image):
    if hasattr(image, "get_flattened_data"):
        data = list(image.get_flattened_data())
    else:
        data = list(image.getdata())

    return [[pixel] if isinstance(pixel, int) else list(pixel) for pixel in data]


def pathSHA1(path):
    digest = hashlib.sha1()

    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def log(message):
    stream = getattr(sys, "__stdout__", None)

    if stream is None:
        return

    stream.write(str(message))
    stream.flush()


def magicParticlesAtlasFiles(path):
    runtime = tool_path("AstralaxRuntime")

    with tempfile.TemporaryDirectory(prefix="mengine-astralax-") as directory:
        result_path = os.path.join(directory, "atlas.info")
        _run_native(
            "AstralaxCompiler",
            (
                "--inspect",
                "--in_path",
                _absolute(path),
                "--runtime_path",
                runtime,
                "--result_path",
                result_path,
            ),
        )

        with open(result_path, "r", encoding="utf-8") as stream:
            lines = [line.rstrip("\r\n") for line in stream]

    try:
        atlas_count = int(lines[0])
    except (IndexError, ValueError) as exception:
        raise RuntimeError("AstralaxCompiler produced invalid atlas metadata") from exception

    expected_lines = 1 + atlas_count * 5

    if len(lines) != expected_lines:
        raise RuntimeError(
            "AstralaxCompiler produced incomplete atlas metadata: expected %d lines, got %d"
            % (expected_lines, len(lines))
        )

    return [lines[1 + index * 5] for index in range(atlas_count)]
