# JSON Schema — Essential Syntax Reference

This is a reference checklist of the JSON Schema keywords generally considered essential for practical use. It's background context for JSSN's design — a target list of what JSSN aims to eventually provide shorthand for, not a description of JSSN itself.

Since JSSN targets **JSON Schema Draft 2020-12** (see the [project README](../README.md)), the sections below describe 2020-12 syntax. Older-draft keywords that were renamed or replaced by 2020-12 are collected separately at the end, for recognition rather than as targets for JSSN.

## Basic Structure

- `$schema` — declares which draft/dialect a document conforms to
- `$id` — the schema's own identifier
- `type` — the fundamental type constraint (`string`, `number`, `integer`, `boolean`, `object`, `array`, `null`)

## Object Validation

- `properties` — per-key schemas
- `required` — array of keys that must be present
- `additionalProperties` — whether, or under what schema, properties not listed in `properties` are allowed
- `patternProperties` — schemas for keys matching a regular expression
- `minProperties` / `maxProperties` — bounds on the number of properties

## Array Validation

- `items` — a single schema constraining every array element, or (when `prefixItems` is also present) every element past the positions `prefixItems` covers
- `prefixItems` — positional/tuple element schemas
- `minItems` / `maxItems` — bounds on array length
- `uniqueItems` — disallow duplicate elements
- `contains` — at least one array element must validate against this schema
- `minContains` / `maxContains` — bounds on how many elements must match `contains` (default: at least one, no upper bound)

## Value Constraints

- `minLength` / `maxLength` / `pattern` — string constraints
- `minimum` / `maximum` / `exclusiveMinimum` / `exclusiveMaximum` / `multipleOf` — number constraints
- `enum` — value must be one of a fixed set of values
- `const` — value must equal one specific fixed value
- `format` — well-known string formats (e.g. `email`, `date-time`, `uri`); advisory by spec, and not always enforced by validators

## Combinators

- `allOf` / `anyOf` / `oneOf` / `not` — schema composition
- `if` / `then` / `else` — conditional validation

## Reuse

- `$defs` — named sub-schemas for reuse
- `$ref` — a reference to a schema, typically one defined under `$defs`

## Documentation / Annotation Keywords

- `title` / `description` — non-validating documentation
- `default` — the value to use when none is provided; documentation only, validators don't inject it automatically
- `examples` — sample values; documentation only, not enforced

## Relational / Conditional Requirements

- `dependentRequired` — "if key A is present, key B must be present too"
- `dependentSchemas` — "if key A is present, the whole instance must also satisfy this schema"

## Not Part of the 2020-12 Draft (Older-Draft Syntax)

These come from earlier drafts (mainly Draft 7) and were renamed or replaced by the time of 2020-12. They aren't reference targets for JSSN's own syntax, but are listed here for recognition, since a lot of JSON Schema written in the wild still uses them.

- `items` as an array of schemas — Draft 7's way of writing positional/tuple validation; replaced by `prefixItems` in 2020-12
- `additionalItems` — Draft 7's companion keyword, constraining elements beyond the tuple; replaced by `items` (single schema) in 2020-12
- `definitions` — Draft 7's name for reusable sub-schemas; renamed to `$defs` starting with draft 2019-09
- `dependencies` — Draft 7's single keyword covering both "if A is present, B must be too" and "if A is present, satisfy this schema"; split into `dependentRequired` and `dependentSchemas` starting with draft 2019-09
