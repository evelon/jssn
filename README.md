한국어 버전은 [README.ko.md](README.ko.md)를 참고하세요.

# JSSN

JSSN (JSON Schema Simplified Notation) is a notation being developed to express the schema of data represented in JSON. Its aim is to complement JSON Schema rather than replace it.

JSSN follows two design principles: compatibility with JSON Schema, and readability.

JSSN's spec is organized as one document per feature — see [spec/README.md](spec/README.md) for what's currently covered and what's on the roadmap. A JSON Schema → JSSN converter implementing the covered syntax is also available — see [converter/README.md](converter/README.md) for usage. See `spec/CHANGELOG.md` and `converter/CHANGELOG.md` for details.

Note: the files under [examples/](examples/) are still pinned to spec v0.1.0, the version the converter currently tracks. This is a known gap that needs fixing — see [#24](https://github.com/evelon/jssn/issues/24).
