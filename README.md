# Mengine-Builder

Mengine-Builder is the Python 3.11+ resource and packaging builder used by
Mengine projects. It replaces the retired resource-builder executable.
Native tools, SDKs, game configurations and game-specific batch files are not
stored in this repository.

## Usage

Install Pillow with the same interpreter that runs the builder:

```text
py -3 -m pip install --user -r requirements.txt
```

Run an existing build configuration without a wrapper executable:

```text
python MengineBuilder.py -path_config <config.json> [-new_var <name>:<value>]
```

Before switching a build machine, populate a clean cache and verify every
managed tool for that platform:

```text
python scripts/verify_install.py --cache <empty-cache-directory>
```

On Apple Silicon, use a Homebrew Python explicitly when the system `python3`
is older than 3.11:

```text
/opt/homebrew/bin/python3.14 MengineBuilder.py -path_config <config.json>
```

The legacy executable `run run` prefix is intentionally unsupported.

`ResourceTiledMap` from Mengine's `TiledMapPlugin` keeps Tiled JSON
(`.tmj`/`.json`) unchanged and copies its external JSON tilesets
(`.tsj`/`.json`) with their relative paths preserved for direct runtime loading.

## Tool resolution and cache

Only tools required by the selected configuration are resolved. Resolution is
strictly ordered:

1. `MENGINE_BUILDER_TOOL_<NAME>` explicit override;
2. the system resolver for tools marked `system` in `tools-manifest.json`;
3. the local directory for tools marked `external` in `tools-manifest.json`;
4. the exact managed package version and URL pinned in the manifest.

Managed archives are downloaded to `.cache/downloads`, verified with SHA-256,
and installed under `.cache/tools/<package>/<version>/<platform-arch>`. A warm
cache does not access the network. Extraction rejects absolute paths, parent
traversal, links and device entries. Concurrent jobs share an interprocess
lock, and a package becomes visible only after an atomic rename.

Set `MENGINE_BUILDER_CACHE` to move the cache or
`MENGINE_BUILDER_MANIFEST` to exercise a test manifest. Both are optional.
`.cache` is ignored by Git and must not be deleted by Jenkins update scripts.

External licensed runtimes live outside the managed cache under
`.local-tools/<package>/<version>/<platform-arch>`. Set
`MENGINE_BUILDER_EXTERNAL_TOOLS` to use a shared machine directory instead.
Builder validates pinned files but never downloads or deletes this directory.

Managed releases never float to `latest`. Updating a tool requires a new
immutable release asset and a reviewed manifest change with its SHA-256.

## System and licensed tools

- Windows `rc.exe` is found on `PATH` or through the installed Windows SDK.
- Windows Python 2 bytecode compilation uses `py -2`.
- `PVRTexToolCLI` is not redistributed. Install the Imagination PowerVR SDK
  and add the command to `PATH`, or set
  `MENGINE_BUILDER_TOOL_PVRTEXTOOLCLI` when a PVRTC build requests it.
- Resource Hacker is downloaded directly from the author's site and pinned by
  SHA-256. Its license prohibits third-party redistribution.
PTZ, DZZ and AEZ packaging is handled by the common `MengineConverter`
aliases `ptc2ptz`, `dzb2dzz` and `aeb2aez`; the managed tools bundle has no
Astralax SDK or runtime dependency.

macOS supports Apple Silicon `arm64`. Windows supports x64. The DX11 shader
converters `text2vso11` and `text2pso11` remain Windows-only; resource
rewriting removes obsolete DX9 shader converters and unsupported platform
artifacts.

## PNG premultiplication and resource-only builds

`img_premultiply: true` enables the native PNG stage even when `png_opt` is false.
It runs before atlas packing, resizing and format conversion. Register source
PNGs as `ResourceImageDefault` in XML/JSON resource descriptions. `File.Premultiply`
describes the source: omitted/0 is straight alpha, 1 is already premultiplied.
The latter is copied without another PMA or alpha-spreading pass. With PMA enabled,
Builder transforms the copied PNG and sets `Premultiply=1` only in output
declarations. PNG preprocessing preserves the original filename and package-relative
`File.Path`; no suffix is added. With only `png_opt` enabled, the PMA flag stays
unchanged. Source images and source declarations are never modified.

Images with the same source and conversion parameters share a native job.
Intermediate files live for one build and are removed on success or failure;
internal `__Dir` paths are excluded from serialized resource descriptions.
Conversion failures stop the build before resource export.

For projects whose SDK/application packaging is handled elsewhere:

```python
from Builder.Build import build_resource_pack
build_resource_pack(source_resources, unpublished_staging,
                    description="Package.xml", img_premultiply=True)
```

This API reuses the PNG and resource-export actions, retains PNG format and
leaves SDK packaging and final directory publication to its caller. The caller
must use unpublished staging and publish it only after success. Calls in one
process are sequential; each starts with fresh conversion and operation caches.

Resource-only builds can also pass `make_atlas=True`, `atlas_max_width=1024`,
`atlas_max_height=1024` and `atlas_rotate=False`. Existing `NoAtlas` declarations
are respected. Atlas parents are lazily compiled (`Precompile=0`). PNGs retain
their source dimensions. Source files are not changed.
Apps using custom UV sampling must handle atlas bounds/rotation, and async
loaders must prefetch the parent texture rather than a sub-image's empty content.
Atlas parents preserve the source PMA flag. Straight-alpha and PMA images must
use separate atlas sections (DataBlocks/tags), or `img_premultiply=True` must
normalize the inputs before packing. Mixed sections and images too large for
the requested page dimensions fail the build before resource export.

Premultiplication needs an AlphaSpreading whose PNG reader widens RGB and
palette inputs to RGBA; `tools-v1.0.6` is the first release that carries it.
`MENGINE_BUILDER_TOOL_ALPHASPREADING` overrides the managed binary when a
locally built one is needed. No managed-cache replacement is performed by
Builder.

## Releases and licenses

Mengine-owned executables come from the `tools-v*` releases in
`irov/Mengine`. Open-source dependency bundles come from the
`dependencies-v*` releases in this repository. Each repackaged archive has a
`LICENSES` directory and `provenance.json`; repository-wide notices are in
`THIRD_PARTY_NOTICES.md`.

`scripts/package_dependency_release.py` reproduces the initial dependency
assets from the audited r444 tool checkout. It is a migration utility, not a
runtime download path.
