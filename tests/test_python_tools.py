import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from PIL import Image

import ProjectBuilder
from PyBuilder import Tools
from PyBuilder.ConfigLoader import ConfigArgumentError, load_build_config, parse_new_variables
from PyBuilder.FileSystem import FileSystem
from PyBuilder.Graph.GraphNodeJson import GraphNodeJson
from PyBuilder.Operation.Operation import Operation
from PyBuilder.Operation.OperationSetExeVersionInfo import OperationSetExeVersionInfo
from PyBuilder.PyCompile import compile27
from PyBuilder.Watcher.Watcher import Watcher
from PyBuilder.WinregCompat import create_macos_winreg
from PyBuilder import Toolchain


class ConfigLoaderTests(unittest.TestCase):
    def test_new_variable_preserves_colons_in_value(self):
        self.assertEqual(parse_new_variables(["-new_var", "url:https://example.test"]), {"url": "https://example.test"})

    def test_load_config_uses_legacy_format_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text('{"dest_dir": "{destination}"}', encoding="utf-8")
            config = load_build_config(path, ["-new_var", "destination:Build Folder"])
            self.assertEqual(config["dest_dir"], "Build Folder")

    def test_invalid_new_variable_is_rejected(self):
        with self.assertRaises(ConfigArgumentError):
            parse_new_variables(["-new_var", "missing_separator"])


class ToolchainTests(unittest.TestCase):
    def test_archive_packaging_uses_common_mengine_converter(self):
        manifest_path = Toolchain.CONSOLE_ROOT / "tools-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        tools = manifest["tools"]
        package_files = manifest["packages"]["mengine-tools"]["platforms"]

        self.assertIn("MengineConverter", tools)
        self.assertNotIn("DazzleCompiler", tools)
        self.assertNotIn("MovieCompiler", tools)
        bundled_files = [path for platform in package_files.values() for path in platform["files"]]
        self.assertTrue(all("DazzleCompiler" not in path for path in bundled_files))
        self.assertTrue(all("MovieCompiler" not in path for path in bundled_files))

    def test_platform_root_is_relative_to_project_builder(self):
        self.assertEqual(Toolchain.platform_root().parent, Toolchain.cache_root())

    def test_windows_only_tool_is_rejected_on_macos(self):
        if Toolchain.platform_name() != "macos":
            self.skipTest("macOS-only assertion")

        with self.assertRaises(Toolchain.UnsupportedPlatformError):
            Toolchain.tool_relative_path("ResourceHacker")

    def test_converter_params_are_stringified(self):
        normalized = Toolchain.normalize_converter_params({"quality": 10, "resize": 0.5})
        self.assertEqual(normalized, {"quality": "10", "resize": "0.5"})

    def test_windows_dependency_hint_uses_active_python(self):
        executable = r"C:\Program Files\Python312\python.exe"

        with mock.patch.object(ProjectBuilder.sys, "platform", "win32"), mock.patch.object(
            ProjectBuilder.sys, "executable", executable
        ):
            expected = '"%s" -m pip install --user Pillow' % executable
            self.assertEqual(ProjectBuilder._dependency_hint(), expected)
            self.assertEqual(Toolchain.dependency_install_hint(), expected)

    def test_python27_is_required_for_python_bytecode_on_macos(self):
        if Toolchain.platform_name() != "macos":
            self.skipTest("macOS-only assertion")

        self.assertIn("python2.7", Toolchain.required_tools_for_config({"python_compile": True}))
        self.assertNotIn("python2.7", Toolchain.required_tools_for_config({"python_compile": False}))

    def test_fxc_shader_converters_are_filtered_on_macos(self):
        if Toolchain.platform_name() != "macos":
            self.skipTest("macOS-only assertion")

        self.assertFalse(Toolchain.converter_supported("text2vso11"))
        self.assertFalse(Toolchain.converter_supported("text2pso"))
        self.assertTrue(Toolchain.converter_supported("text2metallib"))

    def test_python27_compile_uses_bundled_runtime_as_pythonhome(self):
        if Toolchain.platform_name() != "macos":
            self.skipTest("macOS-only assertion")

        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "runtime" / "bin" / "python2.7"
            executable.parent.mkdir(parents=True)
            executable.touch()

            with mock.patch.dict(
                os.environ,
                {"MENGINE_BUILDER_TOOL_PYTHON2_7": str(executable)},
            ), mock.patch("PyBuilder.PyCompile.OSSystem.run", return_value=(True, "", "")) as run:
                self.assertTrue(compile27("Scripts/Unicode path.py"))

            command = run.call_args.args[0]
            environment = run.call_args.kwargs["env"]

            self.assertNotIn("-E", command)
            self.assertEqual(environment["PYTHONHOME"], str(executable.resolve().parent.parent))
            self.assertEqual(environment["PYTHONPATH"], "")


class ImageFacadeTests(unittest.TestCase):
    def test_create_put_get_rotate_and_split(self):
        image = Tools.createImage(2, 1, 4, (0, 0, 0, 0))
        self.assertTrue(Tools.putImageData(image, [[255, 0, 0, 255], [0, 255, 0, 128]]))
        self.assertEqual(Tools.getImageData(image), [[255, 0, 0, 255], [0, 255, 0, 128]])

        rotated = Tools.rotateImage(image, -90)
        self.assertEqual((rotated.width, rotated.height), (1, 2))

        rgb, alpha = Tools.splitImage(image)
        self.assertEqual(rgb.mode, "RGB")
        self.assertEqual([pixel[0] for pixel in Tools.getImageData(alpha)], [255, 128])

    def test_image_file_queries_and_sha1(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.png"
            Image.new("RGBA", (4, 4), (10, 20, 30, 255)).save(path)

            self.assertTrue(Tools.isAlphaInImageFile(path))
            self.assertTrue(Tools.isUselessAlphaInImageFile(path))
            self.assertTrue(Tools.isPow2SquadImageFile(path))
            self.assertEqual(Tools.pathSHA1(path), hashlib.sha1(path.read_bytes()).hexdigest())

    def test_astralax_atlas_inspection_is_not_registered(self):
        with self.assertRaisesRegex(RuntimeError, "was not registered"):
            Tools.magicParticlesAtlasFiles("particle.ptc")


class GraphNodeJsonTests(unittest.TestCase):
    def test_create_front_and_nested_children_preserve_json_shape(self):
        document = {"Resource": [{"Name": "old"}]}
        root = GraphNodeJson("DataBlock", document)

        resource = root.createChildrenFront("Resource")
        resource.setAttribute("Name", "atlas")
        file_node = resource.createChildren("File")
        file_node.setAttribute("Path", "Atlas/smoke.webp")

        self.assertEqual(document["Resource"][0]["Name"], "atlas")
        self.assertEqual(document["Resource"][0]["File"], {"Path": "Atlas/smoke.webp"})
        self.assertEqual(document["Resource"][1]["Name"], "old")


class FileSystemTests(unittest.TestCase):
    def test_copy_dir_does_not_mask_portable_oserror_with_winerror(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            destination = Path(directory) / "destination"

            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(FileNotFoundError):
                    FileSystem.copyDirRecursive(missing, destination)


class ExeVersionInfoTests(unittest.TestCase):
    def test_resource_compiler_files_use_an_isolated_temporary_directory(self):
        operation = OperationSetExeVersionInfo()
        operation.onParams(
            {
                "Version": "1,2,3,4",
                "CompanyInfo": "Wonderland",
                "SourcePath": "Game.exe",
                "Description": "Game",
            }
        )
        temporary_paths = []

        def run_tool(name, *arguments):
            if name == "rc":
                compiler_resource = Path(arguments[-1])
                resource = Path(arguments[-2])
                self.assertTrue(compiler_resource.is_file())
                self.assertEqual(arguments[-3], "/fo")
                self.assertNotIn(str(Toolchain.CONSOLE_ROOT / ".cache"), str(compiler_resource))
                resource.write_bytes(b"compiled resource")
                temporary_paths.extend((compiler_resource, resource))
            elif "add" in arguments:
                resource = Path(arguments[arguments.index("-res") + 1])
                self.assertTrue(resource.is_file())

            return True

        with mock.patch(
            "PyBuilder.Operation.OperationSetExeVersionInfo.OSSystem.tool",
            side_effect=run_tool,
        ):
            self.assertTrue(operation.run())

        self.assertTrue(temporary_paths)
        self.assertTrue(all(path.exists() is False for path in temporary_paths))


class WinregCompatTests(unittest.TestCase):
    def test_registration_is_exposed_through_legacy_winreg_api(self):
        class Registration:
            name = "MonkeyJob"

            def as_mapping(self):
                return {
                    "MENGINE_PROJECT_PATH": "/Volumes/Project/",
                    "MENGINE_PARAMS_PATH": "/Volumes/Params/",
                    "MENGINE_ART_PATH": "/Volumes/Art/",
                }

        class Storage:
            def list_projects(self):
                return [Registration()]

        winreg = create_macos_winreg(Storage())
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Mengine\MonkeyJob")

        self.assertEqual(winreg.QueryValueEx(key, "MENGINE_PROJECT_PATH"), ("/Volumes/Project/", winreg.REG_SZ))

        with self.assertRaises(FileNotFoundError):
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Mengine\Missing")


class WatcherTests(unittest.TestCase):
    def test_operation_exception_restores_interval_stack(self):
        class FailingOperation(Operation):
            def _onRun(self):
                raise RuntimeError("expected failure")

        Watcher.stackIntervals = []
        Watcher.timeIntervals = []

        with self.assertRaisesRegex(RuntimeError, "expected failure"):
            FailingOperation().run()

        self.assertEqual(Watcher.stackIntervals, [])


if __name__ == "__main__":
    unittest.main()
