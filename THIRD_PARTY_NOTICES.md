# Third-party notices

Mengine-Builder contains Python source derived from the former resource builder
in MengineTools. The source in this repository is licensed under MIT.

Native tools are not stored in Git. They are downloaded from immutable URLs
listed in `tools-manifest.json`, verified with SHA-256, and cached locally.
Each published dependency archive includes its own `LICENSES` and provenance
metadata. The relevant upstream projects are:

- FFmpeg and ffprobe: https://ffmpeg.org/
- WebP `cwebp`: https://chromium.googlesource.com/webm/libwebp/
- crunch: https://github.com/BinomialLLC/crunch
- yamdi: https://github.com/ioppermann/yamdi
- TinyPy compiler: https://github.com/irov/tinypy (includes CPython-derived
  components under the PSF license; notices ship with the native tools)
- Resource Hacker: https://www.angusj.com/resourcehacker/

PVRTexToolCLI is separately licensed by Imagination Technologies and is never
downloaded or redistributed by Mengine-Builder.
