# Changelog

This file documents notable changes to the JSSN specification (spec/). The converter maintains its own, independently versioned CHANGELOG.md.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] - 2026-08-22

### Added

- Tuple length syntax: open vs. closed tuples (`...type` / bare `...`), bounded trailing elements, extending a tuple by exactly one element, and edge cases like unreachable elements and inside-out tuples
- `json-schema-reference.md`: a checklist of JSON Schema Draft 2020-12's essential keywords, used to scope JSSN's own roadmap

### Changed

- Feature documents (`types.md`, `required.md`, `tuple-length.md`) now live under `spec/features/`, separate from spec-level docs (`README.md`, `indentation.md`, `json-schema-reference.md`)
- `types.md`'s Array section now points to `tuple-length.md` for the full items-family spec

## [0.1.1] - 2026-08-16

### Added

- Required and optional property syntax: append `!` to a key name to mark it required; properties are optional by default
- `any` type, for values with no type constraint — covers the case of a key that is required but has no corresponding entry in `properties`

### Changed

- Split the spec into one document per feature (`types.md`, `required.md`), with a `README.md` index and roadmap
- Each feature document (and relevant sub-sections) now notes the JSON Schema keyword or element it corresponds to

## [0.1.0] - 2026-08-16

### Added

- Indentation recommendations
- Basic type rules

[0.2.0]: https://github.com/evelon/jssn/compare/spec-v0.1.1...spec-v0.2.0
[0.1.1]: https://github.com/evelon/jssn/compare/spec-v0.1.0...spec-v0.1.1
[0.1.0]: https://github.com/evelon/jssn/releases/tag/spec-v0.1.0
