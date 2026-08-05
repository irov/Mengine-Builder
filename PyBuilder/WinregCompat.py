import sys
import types
from pathlib import Path


REGISTRY_PREFIX = "Software\\Mengine\\"


class _RegistryKey:
    def __init__(self, values=None):
        self.values = values or {}

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception, traceback):
        del exception_type, exception, traceback
        return False


def _registration_export_root():
    return Path(__file__).resolve().parents[2] / "RegistrationExport"


def _load_storage():
    registration_export_root = str(_registration_export_root())

    if registration_export_root not in sys.path:
        sys.path.insert(0, registration_export_root)

    from registration_export.storage import create_storage

    return create_storage()


def create_macos_winreg(storage):
    module = types.ModuleType("winreg")
    module.HKEY_CURRENT_USER = object()
    module.HKEY_CLASSES_ROOT = object()
    module.REG_SZ = 1

    def open_key(root, path, *args, **kwargs):
        del args, kwargs

        if root is module.HKEY_CLASSES_ROOT and path == "":
            return _RegistryKey()

        if root is not module.HKEY_CURRENT_USER or path.startswith(REGISTRY_PREFIX) is False:
            raise FileNotFoundError(path)

        project_name = path[len(REGISTRY_PREFIX):]

        for registration in storage.list_projects():
            if registration.name == project_name:
                return _RegistryKey(registration.as_mapping())

        raise FileNotFoundError(path)

    def query_value_ex(key, name):
        try:
            return key.values[name], module.REG_SZ
        except KeyError as exception:
            raise FileNotFoundError(name) from exception

    def enum_key(key, index):
        del key, index
        raise OSError("no registry subkeys on macOS")

    module.OpenKey = open_key
    module.QueryValueEx = query_value_ex
    module.EnumKey = enum_key
    module.CloseKey = lambda key: None
    return module


def install_macos_winreg(storage=None):
    if sys.platform != "darwin":
        return None

    module = create_macos_winreg(storage or _load_storage())
    sys.modules["winreg"] = module
    return module
