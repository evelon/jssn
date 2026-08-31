# Object

> **JSON Schema equivalent:** the `object` type, together with `properties`, `required`, `additionalProperties`, `patternProperties`, `minProperties`, and `maxProperties`.

As explained in [types.md](types.md), the basic syntax of a JSSN `obj` is as follows.

```jssn
{
  name: str
  email: str
  age: int
}
```

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "additionalProperties": false
}
```

## Required and Optional Properties

> **JSON Schema equivalent:** the `required` array, combined with `properties`

To mark a property as required, append `!` to its key name, immediately before the colon.

```jssn
{
  name!: str
  email!: str
  age: int
}
```

Here, `name` and `email` must be present. `age` may be omitted.

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email"]
}
```

The `!` always goes right after the key name — not before it, and not after the type.

```jssn
name!: str
```

not

```jssn
!name: str
```

or

```jssn
name: str!
```

## Nested Objects

Each `obj`, at any depth, has its own independent set of required/optional properties. Marking a property `!` only affects whether it is required within its immediate parent object.

```jssn
{
  title!: str
  meta: {
    tags!: arr
    notes: str
  }
}
```

`meta` itself is optional, but if it is present, `tags` within it is required.

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "meta": {
      "type": "object",
      "properties": {
        "tags": { "type": "array" },
        "notes": { "type": "string" }
      },
      "required": ["tags"]
    }
  },
  "required": ["title"]
}
```

## Required Without a Type Constraint

JSON Schema allows a key to appear in `required` without appearing in `properties` at all — the key must be present, but its value isn't constrained to any particular shape. In JSSN, this is written as a required property typed `any`.

```jssn
{
  id!
  name!: str
}
```

Here, `id` must be present but can hold any JSON value; `name` must be present and must be a string.

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" }
  },
  "required": ["id", "name"]
}
```

Note that `id` appears in `required` but not in `properties` — it's the exact shape described above.

## Design Notes

- **Optional by default** matches JSON Schema's own default (properties are optional unless listed in `required`), rather than TypeScript's required-by-default convention.
- **Not `?` for optional.** Marking optional properties with `?` (required-by-default, like TypeScript) was considered, but rejected for now: it would flip the default away from JSON Schema's optional-by-default semantics, and it would use up `?`, which may be wanted later for a nullable-value shorthand (e.g. `str?` meaning "string or null").

## Additional Properties

> **JSON Schema equivalent:** `additionalProperties`

JSSN's default form has `additionalProperties` set to `false`. If `additionalProperties` is absent or `true`, write it as follows.

```jssn
{
  name: str
  email: str
  age: int
  ...
}
```

Here, `...` is the omitted form of `any`, as in:

```jssn
{
  name: str
  email: str
  age: int
  ...: any
}
```

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  }
}
```

If `additionalProperties` is a type (schema), write it as follows.

```jssn
{
  name: str
  email: str
  age: int
  ...: str
}
```

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "additionalProperties": { "type": "string" }
}
```

## Pattern Properties

> **JSON Schema equivalent:** `patternProperties`

In JSON Schema, `patternProperties` controls keys via a regexp. In JSSN, a regexp wrapped in `/` goes in the key position. Since `/` is used as the delimiter, any `/` inside the regexp must be escaped.

```jssn
{
  /^S_/: str
  /^I_/: int
}
```

Equivalent to:

```json
{
  "type": "object",
  "patternProperties": {
    "^S_": { "type": "string" },
    "^I_": { "type": "integer" }
  },
  "additionalProperties": false
}
```

When pattern properties and regular properties are used together, putting pattern properties on top is recommended, though this may be relaxed for readability.

```jssn
{
  /^S_/: str
  S_name
  S_email
  /^I_/: int
  I_age
}
```

## Object Size

> **JSON Schema equivalent:** `minProperties`, `maxProperties`

Unlike `arr`, whose elements sit at fixed positions and so can carry a count inside `[]`, `obj` only holds key-name and value-type constraints inside `{}`. A count constraint is a different kind of constraint, so it's written outside `{}`.

`minProperties`/`maxProperties` in JSON Schema constrain the total number of properties on an object, regardless of whether they're named, pattern, or additional properties. JSSN reuses the `min..max` notation covered in [array.md](array.md) for this, wrapped in parentheses and placed right before the `{` that opens the obj body: `(min..max) {`.

```jssn
(3..5) {
  name: str
  email: str
  age: int
  ...
}
```

Equivalent to:

```json
{
  "type": "object",
  "minProperties": 3,
  "maxProperties": 5,
  "properties": {
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  }
}
```

## Out of Scope (For Now)

- `propertyNames` may go between the size and the obj body (`{}`). The details are still undecided.
- Relational/conditional requirements — e.g. "if property A is present, property B is required" (JSON Schema's `dependentRequired`, `dependentSchemas`, `if`/`then`/`else`) — are not covered here. These describe a relationship between properties rather than a property of a single key, so they will need their own construct rather than extending `!`.
