#!/usr/bin/env python3

import argparse
import gzip
import hashlib
import json
import shutil
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path


LICENSE_URLS = {
    "FFmpeg.txt": "https://raw.githubusercontent.com/FFmpeg/FFmpeg/n8.1.2/COPYING.GPLv3",
    "FFmpeg-LICENSE.txt": "https://raw.githubusercontent.com/FFmpeg/FFmpeg/n8.1.2/LICENSE.md",
    "WebP.txt": "https://raw.githubusercontent.com/webmproject/libwebp/v1.6.0/COPYING",
    "crunch.txt": "https://raw.githubusercontent.com/BinomialLLC/crunch/36479bc697be19168daafbf15f47f3c60ccec004/license.txt",
    "yamdi.txt": "https://raw.githubusercontent.com/ioppermann/yamdi/dbf0782342d76808c9aef3cabb7290033273ad43/LICENSE",
}

FFMPEG_THIRD_PARTY = """# FFmpeg bundle components

The Windows binaries are the GPLv3 `2025-07-21-git-8cdb47e47a`
essentials build from gyan.dev, a binary provider linked by ffmpeg.org.

The macOS arm64 bundle is FFmpeg Full 8.1.2_2 and its Homebrew runtime
libraries. It was configured with `--enable-gpl --enable-version3`; the
combined FFmpeg binary is distributed under GPLv3. Individual runtime library
copyright and license metadata is maintained by the corresponding Homebrew
formula and upstream project. The exact library filenames and SHA-256 values
are recorded in `provenance.json` so the formula/source can be identified.

Source offer and build references:

- FFmpeg 8.1.2 source: https://ffmpeg.org/releases/ffmpeg-8.1.2.tar.xz
- FFmpeg license details: https://ffmpeg.org/legal.html
- Homebrew formula metadata: https://formulae.brew.sh/
- gyan.dev build documentation: https://www.gyan.dev/ffmpeg/builds/
"""


PACKAGE_SPECS = (
    ("ffmpeg-windows-x64.zip", "win32/tools/ffmpeg", "zip", ("FFmpeg.txt", "FFmpeg-LICENSE.txt"), "FFmpeg 2025-07-21 gyan.dev essentials"),
    ("ffmpeg-macos-arm64.tar.gz", "macos/tools/ffmpeg", "tar.gz", ("FFmpeg.txt", "FFmpeg-LICENSE.txt"), "FFmpeg Full 8.1.2_2 Homebrew relocatable bundle"),
    ("webp-windows-x64.zip", "win32/tools/webp", "zip", ("WebP.txt",), "WebP cwebp"),
    ("webp-macos-arm64.tar.gz", "macos/tools/webp", "tar.gz", ("WebP.txt",), "WebP 1.6.0 Homebrew relocatable bundle"),
    ("crunch-windows-x64.zip", "win32/tools/crunch", "zip", ("crunch.txt",), "crunch 3.6"),
    ("crunch-macos-arm64.tar.gz", "macos/tools/crunch", "tar.gz", ("crunch.txt",), "crunch 3.6 arm64"),
    ("yamdi-windows-x64.zip", "win32/tools/yamdi", "zip", ("yamdi.txt",), "yamdi 1.9"),
    ("yamdi-macos-arm64.tar.gz", "macos/tools/yamdi", "tar.gz", ("yamdi.txt",), "yamdi 1.9 arm64"),
    ("python27-macos-arm64.tar.gz", "macos/tools/python2.7", "tar.gz", (), "CPython 2.7.18 minimal relocatable arm64 runtime"),
)


def sha256(path):
    digest = hashlib.sha256()

    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def download_licenses(directory):
    result = {}

    for name, url in LICENSE_URLS.items():
        destination = directory / name
        request = urllib.request.Request(url, headers={"User-Agent": "Mengine-Builder release packager"})

        with urllib.request.urlopen(request, timeout=30) as response, destination.open("wb") as output:
            shutil.copyfileobj(response, output)

        result[name] = destination

    return result


def copy_tree(source, staging):
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        destination = staging / relative

        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
        else:
            raise RuntimeError("unsupported source entry: %s" % path)


def provenance(staging, source_label, description):
    files = []

    for path in sorted(staging.rglob("*")):
        if path.is_file() and path.name != "provenance.json":
            files.append(
                {
                    "path": path.relative_to(staging).as_posix(),
                    "sha256": sha256(path),
                    "size": path.stat().st_size,
                }
            )

    return {
        "schema_version": 1,
        "description": description,
        "migration_source": "MengineTools r444 audited checkout",
        "source_directory": source_label,
        "files": files,
    }


def write_archive(staging, output, archive_type):
    if archive_type == "zip":
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    info = zipfile.ZipInfo(path.relative_to(staging).as_posix(), (1980, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = (path.stat().st_mode & 0xFFFF) << 16
                    archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        return

    with output.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w") as archive:
            for path in sorted(staging.rglob("*")):
                if path.is_file() is False:
                    continue

                info = archive.gettarinfo(path, arcname=path.relative_to(staging).as_posix())
                info.mtime = 0
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""

                with path.open("rb") as source:
                    archive.addfile(info, source)


def package(source_root, output_root):
    output_root.mkdir(parents=True, exist_ok=True)
    outputs = []

    with tempfile.TemporaryDirectory(prefix="mengine-builder-licenses-") as licenses_directory:
        licenses = download_licenses(Path(licenses_directory))

        for output_name, relative_source, archive_type, license_names, description in PACKAGE_SPECS:
            source = source_root / relative_source

            if source.is_dir() is False:
                raise FileNotFoundError(source)

            with tempfile.TemporaryDirectory(prefix="mengine-builder-package-") as staging_directory:
                staging = Path(staging_directory)
                copy_tree(source, staging)
                notices = staging / "LICENSES"
                notices.mkdir()

                if output_name.startswith("python27-"):
                    shutil.copy2(source / "LICENSE.txt", notices / "Python-2.7.txt")

                for name in license_names:
                    shutil.copy2(licenses[name], notices / name)

                if output_name.startswith("ffmpeg-"):
                    (notices / "THIRD_PARTY.md").write_text(FFMPEG_THIRD_PARTY, encoding="utf-8")

                metadata = provenance(staging, relative_source, description)
                (staging / "provenance.json").write_text(
                    json.dumps(metadata, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                output = output_root / output_name
                write_archive(staging, output, archive_type)
                print("%s  %s" % (sha256(output), output))
                outputs.append(output)

    checksums = [(sha256(path), path.name) for path in outputs]
    (output_root / "SHA256SUMS").write_text(
        "".join("%s  %s\n" % item for item in checksums),
        encoding="utf-8",
    )
    (output_root / "dependency-build-provenance.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "release": "dependencies-v1.0.0",
                "migration_source": "MengineTools r444 audited checkout",
                "archives": [
                    {"name": name, "sha256": checksum}
                    for checksum, name in checksums
                ],
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dependency-source",
        required=True,
        type=Path,
        help="directory containing the legacy win32/tools and macos/tools trees",
    )
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    package(arguments.dependency_source.resolve(), arguments.output.resolve())


if __name__ == "__main__":
    main()
