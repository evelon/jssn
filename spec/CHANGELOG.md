# Changelog

This file documents notable changes to the JSSN specification (spec/). The converter maintains its own, independently versioned CHANGELOG.md.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.1] - 2026-08-16

### Added

- Required and optional property syntax: append `!` to a key name to mark it required; properties are optional by default
- `any` type, for values with no type constraint — covers the case of a key that is required but has no corresponding entry in `properties`

### Changed

- Split the spec into one document per feature (`types.md`, `required-optional-properties.md`), with a `README.md` index and roadmap
- Each feature document (and relevant sub-sections) now notes the JSON Schema keyword or element it corresponds to

## [0.1.0] - 2026-08-16

### Added

- Indentation recommendations
- Basic type rules
