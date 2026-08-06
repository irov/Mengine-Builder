import hashlib
import json
import multiprocessing
import os
from pathlib import Path
import shutil
import tempfile
import time
import unittest
import zipfile
from unittest import mock

from PyBuilder.ToolInstaller import (
    DownloadError,
    ChecksumError,
    ManifestError,
    PackageLock,
    ToolInstaller,
    ToolInstallerError,
    UnsafeArchiveError,
)


def _hold_lock(path, ready):
    with PackageLock(path, timeout=5):
        ready.set()
        time.sleep(0.5)


class LocalInstaller(ToolInstaller):
    def __init__(self, *args, source_archive, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_archive = Path(source_archive)
        self.downloads = 0
        self.fail_download = False

    def _download(self, url, destination):
        self.downloads += 1

        if self.fail_download:
            destination.write_bytes(b"partial")
            raise OSError("interrupted")

        shutil.copyfile(self.source_archive, destination)


class ToolInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.archive = self.root / "tool.zip"
        self._write_archive({"bin/tool": b"tool", "runtime.dll": b"runtime"})
        self.manifest_path = self.root / "tools-manifest.json"
        self._write_manifest()

    def tearDown(self):
        self.temporary.cleanup()

    def _write_archive(self, files):
        with zipfile.ZipFile(self.archive, "w") as archive:
            for name, content in files.items():
                archive.writestr(name, content)

    def _write_manifest(self, **platform_overrides):
        package_platform = {
            "url": "https://downloads.example.test/tool-v1.zip",
            "sha256": hashlib.sha256(self.archive.read_bytes()).hexdigest(),
            "archive": "zip",
            "files": ["bin/tool", "runtime.dll"],
            "executables": ["bin/tool"],
        }
        package_platform.update(platform_overrides)
        manifest = {
            "schema_version": 1,
            "packages": {
                "test-package": {
                    "version": "v1.0.0",
                    "platforms": {"test-platform": package_platform},
                }
            },
            "tools": {
                "test-tool": {
                    "test-platform": {
                        "kind": "managed",
                        "package": "test-package",
                        "path": "bin/tool",
                    }
                },
                "system-tool": {
                    "test-platform": {
                        "kind": "system",
                        "candidates": ["missing-test-command"],
                        "hint": "install the test SDK",
                    }
                },
                "external-tool": {
                    "test-platform": {
                        "kind": "external",
                        "package": "licensed-sdk",
                        "version": "v2.0.0",
                        "path": "runtime.bin",
                        "sha256": hashlib.sha256(b"external").hexdigest(),
                    }
                },
            },
        }
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def _installer(self):
        return LocalInstaller(
            self.root,
            "test-platform",
            manifest_path=self.manifest_path,
            cache_root=self.root / "cache",
            source_archive=self.archive,
        )

    def test_first_download_and_cache_hit_without_network(self):
        installer = self._installer()
        path = installer.resolve("test-tool")
        self.assertEqual(path.read_bytes(), b"tool")
        self.assertEqual(installer.downloads, 1)
        self.assertTrue(os.access(path, os.X_OK))

        installer.fail_download = True
        self.assertEqual(installer.resolve("test-tool"), path)
        self.assertEqual(installer.downloads, 1)

    def test_missing_package_file_is_repaired_from_download_cache(self):
        installer = self._installer()
        path = installer.resolve("test-tool")
        path.unlink()
        installer.fail_download = True

        repaired = installer.resolve("test-tool")
        self.assertEqual(repaired.read_bytes(), b"tool")
        self.assertEqual(installer.downloads, 1)

    def test_wrong_sha_leaves_no_archive_or_installed_package(self):
        self._write_manifest(sha256="f" * 64)
        installer = self._installer()

        with self.assertRaises(ChecksumError):
            installer.resolve("test-tool")

        self.assertEqual(list((self.root / "cache").rglob("*.part")), [])
        self.assertEqual(list((self.root / "cache" / "tools").rglob(".complete.json")), [])

    def test_interrupted_download_leaves_no_partial_or_package(self):
        installer = self._installer()
        installer.fail_download = True

        with self.assertRaises(DownloadError):
            installer.resolve("test-tool")

        self.assertEqual(installer.downloads, installer.DOWNLOAD_ATTEMPTS)
        self.assertEqual(list((self.root / "cache").rglob("*.part")), [])
        self.assertEqual(list((self.root / "cache" / "tools").rglob(".complete.json")), [])

    def test_unsafe_archive_path_is_rejected(self):
        self._write_archive({"../outside": b"bad", "bin/tool": b"tool", "runtime.dll": b"runtime"})
        self._write_manifest()
        installer = self._installer()

        with self.assertRaises(UnsafeArchiveError):
            installer.resolve("test-tool")

        self.assertFalse((self.root / "outside").exists())

    def test_override_wins_without_reading_manifest(self):
        override = self.root / "override-tool"
        override.write_bytes(b"override")
        missing_manifest = self.root / "missing.json"
        installer = ToolInstaller(
            self.root,
            "test-platform",
            manifest_path=missing_manifest,
            cache_root=self.root / "cache",
        )

        with mock.patch.dict(os.environ, {"MENGINE_BUILDER_TOOL_TEST_TOOL": str(override)}):
            self.assertEqual(installer.resolve("test-tool"), override.resolve())

    def test_missing_system_tool_has_install_hint(self):
        installer = self._installer()

        with mock.patch("PyBuilder.ToolInstaller.shutil.which", return_value=None):
            with self.assertRaisesRegex(ToolInstallerError, "install the test SDK"):
                installer.resolve("system-tool")

    def test_external_tool_uses_local_directory_without_network(self):
        path = self.root / ".local-tools" / "licensed-sdk" / "v2.0.0" / "test-platform" / "runtime.bin"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"external")
        installer = self._installer()

        self.assertEqual(installer.resolve("external-tool"), path.resolve())
        self.assertEqual(installer.downloads, 0)

    def test_missing_external_tool_has_exact_path_and_override(self):
        installer = self._installer()
        expected = installer.external_root / "licensed-sdk" / "v2.0.0" / "test-platform" / "runtime.bin"

        with self.assertRaises(ToolInstallerError) as context:
            installer.resolve("external-tool")

        self.assertIn(str(expected), str(context.exception))
        self.assertIn("MENGINE_BUILDER_TOOL_EXTERNAL_TOOL", str(context.exception))

    def test_external_tool_sha_is_verified(self):
        path = self.root / ".local-tools" / "licensed-sdk" / "v2.0.0" / "test-platform" / "runtime.bin"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"wrong")

        with self.assertRaisesRegex(ChecksumError, "external tool external-tool"):
            self._installer().resolve("external-tool")

    def test_unknown_schema_platform_and_tool_are_rejected(self):
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        manifest["schema_version"] = 99
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        with self.assertRaises(ManifestError):
            self._installer().resolve("test-tool")

        self._write_manifest()

        with self.assertRaises(ManifestError):
            LocalInstaller(
                self.root,
                "unknown-platform",
                manifest_path=self.manifest_path,
                cache_root=self.root / "cache",
                source_archive=self.archive,
            ).install_package("test-package")

        with self.assertRaises(ManifestError):
            self._installer().resolve("unknown-tool")

    def test_mutable_url_is_rejected(self):
        self._write_manifest(url="https://example.test/releases/latest/download/tool.zip")

        with self.assertRaisesRegex(ManifestError, "mutable URL"):
            self._installer().resolve("test-tool")

    def test_missing_runtime_file_prevents_install(self):
        self._write_archive({"bin/tool": b"tool"})
        self._write_manifest()

        with self.assertRaisesRegex(ToolInstallerError, "runtime.dll"):
            self._installer().resolve("test-tool")

    def test_process_lock_serializes_two_processes(self):
        lock_path = self.root / "cache" / "locks" / "package.lock"
        ready = multiprocessing.Event()
        process = multiprocessing.Process(target=_hold_lock, args=(lock_path, ready))
        process.start()
        self.assertTrue(ready.wait(timeout=3))
        started = time.monotonic()

        with PackageLock(lock_path, timeout=3):
            elapsed = time.monotonic() - started

        process.join(timeout=3)
        self.assertEqual(process.exitcode, 0)
        self.assertGreaterEqual(elapsed, 0.3)


if __name__ == "__main__":
    unittest.main()
