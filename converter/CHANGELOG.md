# Changelog

This file documents notable changes to the JSON Schema → JSSN converter (converter/). The spec maintains its own, independently versioned CHANGELOG.md.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-08-16

### Added

- `json_schema_to_jssn.py`: a CLI that converts a JSON Schema file into JSSN
- Implements the JSSN spec's [0.1.0](../spec/CHANGELOG.md#010---2026-08-16) release (basic type rules)
  - `type` keyword: `string`, `number`, `integer`, `boolean`, `object`, `array`, `null`
  - `properties`, for objects
  - `items` / `prefixItems`, for arrays
- Type inference from `properties` or `items`/`prefixItems` when `type` is omitted
- `prefixItems` preferred over `items` for tuple-style (positional) arrays
- Union `type` arrays resolved by picking the first JSSN-representable member
- `-o`/`--output` option to write the result to a file instead of stdout
- Constructs not yet covered by the JSSN spec (`$ref`, `allOf`/`anyOf`/`oneOf`, `enum`, `const`, `required`, `format`, `additionalProperties`, `default`, etc.) are dropped from the output, with a warning printed to stderr for each dropped property or array item
- Example fixtures (`examples/supported.*`, `examples/with-unsupported.*`) and a test suite covering type aliases, object/array conversion, and the CLI
