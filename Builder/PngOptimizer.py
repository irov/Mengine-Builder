"""Build-scoped queue for the native AlphaSpreading/PMA stage."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
from pathlib import Path
import shutil
import tempfile

from PIL import Image

from Builder.OSSystem import OSSystem
from Builder.Error.ErrorHandler import ErrorHandler


class PngOptimizer:
    def __init__(self, directory):
        Path(directory).mkdir(parents=True, exist_ok=True)
        self.workspace = tempfile.TemporaryDirectory(prefix="png-", dir=directory)
        self.jobs = {}
        self.outputs = {}

    def output_path(self, source, premultiply):
        key = str(Path(source).resolve()) + (":pma" if premultiply else ":spread")
        return str(Path(self.workspace.name) / (hashlib.sha256(key.encode("utf-8")).hexdigest() + ".png"))

    def optimize(self, source, destination, premultiply):
        source, destination = str(Path(source).resolve()), str(Path(destination).resolve())
        if source == destination:
            raise ValueError("PNG preprocessing must not overwrite its source: " + source)
        key = (source, bool(premultiply))
        if destination in self.outputs and self.outputs[destination] != key:
            raise ValueError("Conflicting PNG preprocessing requests: " + destination)
        self.outputs[destination] = key
        destinations = self.jobs.setdefault(key, [])
        if destination not in destinations:
            destinations.append(destination)
        return True

    @staticmethod
    def _convert(job):
        (source, premultiply), destinations = job
        destination = destinations[0]
        try:
            Path(destination).parent.mkdir(parents=True, exist_ok=True)
            arguments = ["--in", source, "--out", destination]
            if premultiply:
                arguments.append("--premultiply")
            success, stdout, stderr = OSSystem.run_tool("AlphaSpreading", arguments)
            if not success:
                raise RuntimeError(stderr.strip() or stdout.strip() or "AlphaSpreading failed")
            with Image.open(destination) as image:
                if image.format != "PNG":
                    raise ValueError("AlphaSpreading did not produce a PNG")
                image.verify()
            for alias in destinations[1:]:
                Path(alias).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(destination, alias)
        except Exception as exception:
            return "%s: %s" % (source, exception)
        return None

    def flush(self):
        if not self.jobs:
            return True
        with ThreadPoolExecutor(max_workers=min(8, len(self.jobs))) as workers:
            failures = [error for error in workers.map(self._convert, self.jobs.items()) if error is not None]
        for error in failures:
            ErrorHandler.warning("PngOptimizer failed: %s", error)
        return not failures

    def cleanup(self):
        self.jobs.clear()
        self.outputs.clear()
        self.workspace.cleanup()
