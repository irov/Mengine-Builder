#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Builder.ToolInstaller import ToolInstaller, ToolInstallerError
from Builder.Toolchain import platform_key


def main():
    parser = argparse.ArgumentParser(
        description="Download and verify every managed Mengine-Builder tool for this platform."
    )
    parser.add_argument("--manifest", type=Path, default=ROOT / "tools-manifest.json")
    parser.add_argument("--cache", type=Path)
    arguments = parser.parse_args()

    current_platform = platform_key()
    installer = ToolInstaller(
        ROOT,
        current_platform,
        manifest_path=arguments.manifest,
        cache_root=arguments.cache,
    )
    managed_tools = []

    for name, platforms in sorted(installer.manifest["tools"].items()):
        tool = platforms.get(current_platform)

        if tool is not None and tool.get("kind") == "managed":
            managed_tools.append(name)

    if not managed_tools:
        print("No managed tools are configured for %s" % current_platform)
        return 1

    try:
        for name in managed_tools:
            path = installer.resolve(name)
            print("%s: %s" % (name, path))
    except ToolInstallerError as exception:
        print("Managed tool verification failed: %s" % exception, file=sys.stderr)
        return 1

    print("Verified %d managed tools for %s" % (len(managed_tools), current_platform))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
