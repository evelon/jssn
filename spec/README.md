# JSSN Spec

This directory contains the JSSN specification, organized as one document per feature. See the [project README](../README.md) for an overview of JSSN.

JSSN's spec targets **JSON Schema Draft 2020-12**. Where syntax differs from older drafts (Draft 7 / 2019-09), the relevant document notes the older-draft equivalent alongside the 2020-12 form.

## Documents

- [indentation.md](./indentation.md) — indentation recommendations
- [json-schema-reference.md](./json-schema-reference.md) — reference checklist of JSON Schema's essential syntax, used to scope JSSN's own roadmap

### Features

- [types.md](./features/types.md) — basic type names and array/object syntax
- [array.md](./features/array.md) — array length and open/closed array syntax (`items`, `prefixItems`, `minItems`, `maxItems`)
- [object.md](./features/object.md) — object syntax: required vs. optional properties (the `!` suffix), `additionalProperties`, `patternProperties`, `minProperties`/`maxProperties`

## Documentation Convention

Each feature document notes, directly under its title (and under relevant sub-sections), the JSON Schema keyword or element the syntax corresponds to, using a `> **JSON Schema equivalent:** ...` blockquote.

## Roadmap (Not Yet Covered)

- Union types / nullable values
- `enum` / `const`
- String, number, and array value constraints (`minLength`, `pattern`, `minimum`, `maximum`, `uniqueItems`, `contains`/`minContains`/`maxContains`, etc.)
- Reuse / references (corresponds to JSON Schema's `$ref`/`$defs`)
- Combinators (`allOf`/`anyOf`/`oneOf`/`not`, `if`/`then`/`else`)
- Relational/conditional required properties (corresponds to JSON Schema's `dependentRequired`/`dependentSchemas`)
- `default` / `examples`
