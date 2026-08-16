# JSSN Spec

This directory contains the JSSN specification, organized as one document per feature. See the [project README](../README.md) for an overview of JSSN.

JSSN's spec targets **JSON Schema Draft 2020-12**. Where syntax differs from older drafts (Draft 7 / 2019-09), the relevant document notes the older-draft equivalent alongside the 2020-12 form.

## Documents

- [types.md](./types.md) — basic type names and array/object syntax
- [required-optional-properties.md](./required-optional-properties.md) — required vs. optional property syntax (the `!` suffix)

## Documentation Convention

Each feature document notes, directly under its title (and under relevant sub-sections), the JSON Schema keyword or element the syntax corresponds to, using a `> **JSON Schema equivalent:** ...` blockquote.

## Roadmap (Not Yet Covered)

- Union types / nullable values
- `enum` / `const`
- String, number, and array value constraints (`minLength`, `pattern`, `minimum`, `maximum`, `minItems`, etc.)
- Reuse / references (corresponds to JSON Schema's `$ref`/`$defs`)
- `additionalProperties` control
- Combinators (`allOf`/`anyOf`/`oneOf`/`not`, `if`/`then`/`else`)
- Relational/conditional required properties (corresponds to JSON Schema's `dependentRequired`/`dependentSchemas`)
- `default` / `examples`
