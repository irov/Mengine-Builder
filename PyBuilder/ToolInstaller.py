import contextlib
import hashlib
import json
import os
import re
import shutil
import stat
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
import uuid
import zipfile
from pathlib import Path, PurePosixPath


class ToolInstallerError(RuntimeError):
    pass


class ManifestError(ToolInstallerError):
    pass


class DownloadError(ToolInstallerError):
    pass


class ChecksumError(ToolInstallerError):
    pass


class UnsafeArchiveError(ToolInstallerError):
    pass


class PackageLock:
    def __init__(self, path, timeout=300.0, stale_after=1800.0):
        self.path = Path(path)
        self.timeout = timeout
        self.stale_after = stale_after

    def __enter__(self):
        deadline = time.monotonic() + self.timeout
        self.path.parent.mkdir(parents=True, exist_ok=True)

        while True:
            try:
                self.path.mkdir()
                (self.path / "owner.json").write_text(
                    json.dumps({"pid": os.getpid(), "created": time.time()}),
                    encoding="utf-8",
                )
                return self
            except FileExistsError:
                try:
                    age = time.time() - self.path.stat().st_mtime
                except FileNotFoundError:
                    continue

                if age > self.stale_after:
                    shutil.rmtree(self.path, ignore_errors=True)
                    continue

                if time.monotonic() >= deadline:
                    raise ToolInstallerError("timed out waiting for tool package lock: %s" % self.path)

                time.sleep(0.1)

    def __exit__(self, exception_type, exception, traceback):
        shutil.rmtree(self.path, ignore_errors=True)


class ToolInstaller:
    SCHEMA_VERSION = 1
    URL_TIMEOUT = 30
    DOWNLOAD_ATTEMPTS = 3

    def __init__(self, root, platform_key, manifest_path=None, cache_root=None):
        self.root = Path(root).resolve()
        self.platform_key = platform_key
        self.manifest_path = Path(
            manifest_path or os.environ.get("MENGINE_BUILDER_MANIFEST", self.root / "tools-manifest.json")
        ).resolve()
        self.cache_root = Path(
            cache_root or os.environ.get("MENGINE_BUILDER_CACHE", self.root / ".cache")
        ).resolve()
        self.external_root = Path(
            os.environ.get("MENGINE_BUILDER_EXTERNAL_TOOLS", self.root / ".local-tools")
        ).resolve()
        self._manifest = None

    @property
    def manifest(self):
        if self._manifest is None:
            try:
                self._manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exception:
                raise ManifestError("unable to read tool manifest %s: %s" % (self.manifest_path, exception)) from exception

            self._validate_manifest(self._manifest)

        return self._manifest

    def resolve(self, name):
        override = os.environ.get(self._override_name(name))

        if override:
            path = Path(override).expanduser().resolve()

            if path.is_file() is False:
                raise ToolInstallerError("tool override %s does not point to a file: %s" % (self._override_name(name), path))

            return path

        try:
            tool = self.manifest["tools"][name]
        except KeyError as exception:
            raise ManifestError("unknown tool: %s" % name) from exception

        platform_tool = tool.get(self.platform_key)

        if platform_tool is None:
            raise ToolInstallerError("%s is unsupported on %s" % (name, self.platform_key))

        kind = platform_tool.get("kind")

        if kind == "system":
            return self._resolve_system(name, platform_tool)

        if kind == "external":
            return self._resolve_external(name, platform_tool)

        if kind != "managed":
            raise ManifestError("tool %s has unknown kind %r" % (name, kind))

        package_root = self.install_package(platform_tool["package"])
        path = package_root / self._relative_path(platform_tool["path"], "tool %s path" % name)

        if path.is_file() is False:
            self._remove_package(package_root)
            package_root = self.install_package(platform_tool["package"])
            path = package_root / self._relative_path(platform_tool["path"], "tool %s path" % name)

        if path.is_file() is False:
            raise ToolInstallerError("package did not provide tool %s: %s" % (name, path))

        return path

    def tool_relative_path(self, name):
        try:
            platform_tool = self.manifest["tools"][name][self.platform_key]
        except KeyError as exception:
            raise ManifestError("tool %s is unsupported on %s" % (name, self.platform_key)) from exception

        if platform_tool.get("kind") != "managed":
            raise ManifestError("non-managed tool %s has no managed relative path" % name)

        return self._relative_path(platform_tool["path"], "tool %s path" % name)

    def install_package(self, package_name):
        package, platform_package = self._package(package_name)
        version = package["version"]
        target = self.cache_root / "tools" / package_name / version / self.platform_key
        archive_hash = platform_package["sha256"].lower()

        if self._package_complete(target, package_name, version, archive_hash, platform_package):
            return target

        lock_name = "%s-%s-%s.lock" % (package_name, self.platform_key, archive_hash[:16])

        with PackageLock(self.cache_root / "locks" / lock_name):
            if self._package_complete(target, package_name, version, archive_hash, platform_package):
                return target

            self._remove_package(target)
            archive = self._obtain_archive(platform_package)
            self._publish_package(target, package_name, version, platform_package, archive)

        return target

    def _package(self, package_name):
        try:
            package = self.manifest["packages"][package_name]
            platform_package = package["platforms"][self.platform_key]
        except KeyError as exception:
            raise ManifestError("package %s is unavailable on %s" % (package_name, self.platform_key)) from exception

        return package, platform_package

    def _package_complete(self, target, package_name, version, archive_hash, platform_package):
        marker = target / ".complete.json"

        try:
            installed = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False

        expected_marker = {
            "package": package_name,
            "version": version,
            "platform": self.platform_key,
            "sha256": archive_hash,
        }

        if installed != expected_marker:
            return False

        return all((target / self._relative_path(path, "expected file")).is_file() for path in platform_package["files"])

    def _obtain_archive(self, platform_package):
        archive_hash = platform_package["sha256"].lower()
        suffix = {"zip": ".zip", "tar.gz": ".tar.gz"}[platform_package["archive"]]
        downloads = self.cache_root / "downloads"
        destination = downloads / (archive_hash + suffix)
        downloads.mkdir(parents=True, exist_ok=True)

        if destination.is_file():
            if self._sha256(destination) == archive_hash:
                return destination

            destination.unlink()

        last_exception = None

        for attempt in range(1, self.DOWNLOAD_ATTEMPTS + 1):
            temporary = downloads / (".%s.%s.part" % (archive_hash, uuid.uuid4().hex))

            try:
                self._download(platform_package["url"], temporary)
                actual_hash = self._sha256(temporary)

                if actual_hash != archive_hash:
                    raise ChecksumError(
                        "SHA-256 mismatch for %s: expected %s, got %s"
                        % (platform_package["url"], archive_hash, actual_hash)
                    )

                os.replace(temporary, destination)
                return destination
            except (OSError, urllib.error.URLError, DownloadError, ChecksumError) as exception:
                last_exception = exception
                temporary.unlink(missing_ok=True)

                if isinstance(exception, ChecksumError):
                    break

                if attempt < self.DOWNLOAD_ATTEMPTS:
                    time.sleep(0.25 * attempt)

        if isinstance(last_exception, ChecksumError):
            raise last_exception

        raise DownloadError("unable to download %s: %s" % (platform_package["url"], last_exception)) from last_exception

    def _download(self, url, destination):
        request = urllib.request.Request(url, headers={"User-Agent": "Mengine-Builder/1"})

        with urllib.request.urlopen(request, timeout=self.URL_TIMEOUT) as response, destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)

                if not chunk:
                    break

                output.write(chunk)

    def _publish_package(self, target, package_name, version, platform_package, archive):
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".%s-" % target.name, dir=target.parent))

        try:
            self._extract(archive, staging, platform_package["archive"])

            missing = [
                path for path in platform_package["files"]
                if (staging / self._relative_path(path, "expected file")).is_file() is False
            ]

            if missing:
                raise ToolInstallerError(
                    "package %s is missing expected files: %s" % (package_name, ", ".join(missing))
                )

            for path in platform_package.get("executables", []):
                executable = staging / self._relative_path(path, "executable")
                executable.chmod(executable.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

            (staging / ".complete.json").write_text(
                json.dumps(
                    {
                        "package": package_name,
                        "version": version,
                        "platform": self.platform_key,
                        "sha256": platform_package["sha256"].lower(),
                    },
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            os.replace(staging, target)
        finally:
            if staging.exists():
                shutil.rmtree(staging, ignore_errors=True)

    def _extract(self, archive, destination, archive_type):
        if archive_type == "zip":
            with zipfile.ZipFile(archive) as source:
                for member in source.infolist():
                    path = self._safe_member_path(member.filename)
                    mode = member.external_attr >> 16

                    if stat.S_ISLNK(mode):
                        raise UnsafeArchiveError("archive contains a symbolic link: %s" % member.filename)

                    target = destination / path

                    if member.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue

                    target.parent.mkdir(parents=True, exist_ok=True)

                    with source.open(member) as input_file, target.open("wb") as output_file:
                        shutil.copyfileobj(input_file, output_file)

            return

        if archive_type == "tar.gz":
            with tarfile.open(archive, mode="r:gz") as source:
                for member in source.getmembers():
                    path = self._safe_member_path(member.name)
                    target = destination / path

                    if member.isdir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue

                    if member.isfile() is False:
                        raise UnsafeArchiveError("archive contains unsupported entry: %s" % member.name)

                    target.parent.mkdir(parents=True, exist_ok=True)

                    with contextlib.closing(source.extractfile(member)) as input_file, target.open("wb") as output_file:
                        if input_file is None:
                            raise UnsafeArchiveError("unable to extract archive member: %s" % member.name)

                        shutil.copyfileobj(input_file, output_file)

            return

        raise ManifestError("unsupported archive type: %s" % archive_type)

    def _resolve_system(self, name, tool):
        candidates = tool.get("candidates", [])

        for candidate in candidates:
            path = shutil.which(candidate)

            if path:
                return Path(path).resolve()

        if tool.get("resolver") == "windows_sdk":
            path = self._windows_sdk_tool(candidates)

            if path:
                return path

        hint = tool.get("hint", "install it and add it to PATH")
        raise ToolInstallerError("required system tool %s is missing; %s" % (name, hint))

    def _resolve_external(self, name, tool):
        relative_path = self._relative_path(tool["path"], "external tool %s path" % name)
        path = self.external_root / tool["package"] / tool["version"] / self.platform_key / relative_path

        if path.is_file() is False:
            override = self._override_name(name)
            raise ToolInstallerError(
                "required external tool %s is missing; place it at %s or set %s"
                % (name, path, override)
            )

        expected = tool.get("sha256")

        if expected is not None:
            actual = self._sha256(path)

            if actual != expected.lower():
                raise ChecksumError(
                    "SHA-256 mismatch for external tool %s at %s: expected %s, got %s"
                    % (name, path, expected.lower(), actual)
                )

        return path.resolve()

    @staticmethod
    def _windows_sdk_tool(candidates):
        if os.name != "nt":
            return None

        try:
            import winreg
        except ImportError:
            return None

        roots = []

        for access in (winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY):
            try:
                with winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows Kits\Installed Roots",
                    0,
                    winreg.KEY_READ | access,
                ) as key:
                    roots.append(Path(winreg.QueryValueEx(key, "KitsRoot10")[0]))
            except OSError:
                continue

        for root in roots:
            bin_root = root / "bin"

            if bin_root.is_dir() is False:
                continue

            versions = sorted((path for path in bin_root.iterdir() if path.is_dir()), reverse=True)

            for version in versions:
                for architecture in ("x64", "x86"):
                    for candidate in candidates:
                        path = version / architecture / candidate

                        if path.is_file():
                            return path.resolve()

        return None

    def _validate_manifest(self, manifest):
        if manifest.get("schema_version") != self.SCHEMA_VERSION:
            raise ManifestError(
                "unsupported tool manifest schema %r (expected %d)"
                % (manifest.get("schema_version"), self.SCHEMA_VERSION)
            )

        if not isinstance(manifest.get("packages"), dict) or not isinstance(manifest.get("tools"), dict):
            raise ManifestError("tool manifest must contain packages and tools objects")

        for package_name, package in manifest["packages"].items():
            if not re.fullmatch(r"[A-Za-z0-9._-]+", package_name):
                raise ManifestError("invalid package ID: %s" % package_name)

            version = package.get("version")

            if not isinstance(version, str) or not version:
                raise ManifestError("package %s has no version" % package_name)

            platforms = package.get("platforms")

            if not isinstance(platforms, dict):
                raise ManifestError("package %s has no platforms object" % package_name)

            for platform_key, platform_package in platforms.items():
                self._validate_package_platform(package_name, platform_key, platform_package)

        for tool_name, platforms in manifest["tools"].items():
            if not isinstance(platforms, dict):
                raise ManifestError("tool %s must contain platform mappings" % tool_name)

            for platform_key, tool in platforms.items():
                if tool.get("kind") == "managed":
                    package_name = tool.get("package")

                    if package_name not in manifest["packages"]:
                        raise ManifestError("tool %s references unknown package %s" % (tool_name, package_name))

                    if platform_key not in manifest["packages"][package_name]["platforms"]:
                        raise ManifestError("tool %s package is unavailable on %s" % (tool_name, platform_key))

                    self._relative_path(tool.get("path"), "tool %s path" % tool_name)
                elif tool.get("kind") == "system":
                    if not isinstance(tool.get("candidates"), list):
                        raise ManifestError("system tool %s has no candidates list" % tool_name)
                elif tool.get("kind") == "external":
                    package = tool.get("package")
                    version = tool.get("version")

                    if not isinstance(package, str) or re.fullmatch(r"[A-Za-z0-9._-]+", package) is None:
                        raise ManifestError("external tool %s has invalid package ID" % tool_name)

                    if not isinstance(version, str) or not version:
                        raise ManifestError("external tool %s has no version" % tool_name)

                    self._relative_path(tool.get("path"), "external tool %s path" % tool_name)

                    checksum = tool.get("sha256")

                    if checksum is not None and re.fullmatch(r"[0-9a-fA-F]{64}", checksum) is None:
                        raise ManifestError("external tool %s has invalid SHA-256" % tool_name)
                else:
                    raise ManifestError("tool %s has unknown kind %r" % (tool_name, tool.get("kind")))

    def _validate_package_platform(self, package_name, platform_key, package):
        url = package.get("url")

        if not isinstance(url, str) or not url.startswith("https://"):
            raise ManifestError("package %s/%s URL must use HTTPS" % (package_name, platform_key))

        lowered_url = url.lower()

        if "/latest" in lowered_url or "/refs/heads/" in lowered_url or re.search(r"[?&](?:ref|version)=latest(?:&|$)", lowered_url):
            raise ManifestError("package %s/%s uses a mutable URL: %s" % (package_name, platform_key, url))

        checksum = package.get("sha256", "")

        if re.fullmatch(r"[0-9a-fA-F]{64}", checksum) is None:
            raise ManifestError("package %s/%s has invalid SHA-256" % (package_name, platform_key))

        if package.get("archive") not in ("zip", "tar.gz"):
            raise ManifestError("package %s/%s has unsupported archive type" % (package_name, platform_key))

        files = package.get("files")

        if not isinstance(files, list) or not files:
            raise ManifestError("package %s/%s has no expected files" % (package_name, platform_key))

        for path in files + package.get("executables", []):
            self._relative_path(path, "package file")

    @staticmethod
    def _safe_member_path(value):
        path = ToolInstaller._relative_path(value.replace("\\", "/"), "archive member")

        if re.match(r"^[A-Za-z]:", value):
            raise UnsafeArchiveError("archive member uses an absolute drive path: %s" % value)

        return path

    @staticmethod
    def _relative_path(value, description):
        if not isinstance(value, str) or not value:
            raise ManifestError("%s must be a non-empty string" % description)

        if "\\" in value or re.match(r"^[A-Za-z]:", value):
            raise UnsafeArchiveError("unsafe %s: %s" % (description, value))

        path = PurePosixPath(value)

        if path.is_absolute() or ".." in path.parts or "." in path.parts:
            raise UnsafeArchiveError("unsafe %s: %s" % (description, value))

        return Path(*path.parts)

    @staticmethod
    def _override_name(name):
        normalized = re.sub(r"[^A-Za-z0-9]", "_", name).upper()
        return "MENGINE_BUILDER_TOOL_%s" % normalized

    @staticmethod
    def _sha256(path):
        digest = hashlib.sha256()

        with Path(path).open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)

        return digest.hexdigest()

    def _remove_package(self, path):
        path = Path(path).resolve()
        tools_root = (self.cache_root / "tools").resolve()

        if tools_root not in path.parents:
            raise ToolInstallerError("refusing to remove package outside cache: %s" % path)

        shutil.rmtree(path, ignore_errors=True)
