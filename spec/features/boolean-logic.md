# Boolean Logic

> **JSON Schema equivalent:** `allOf`, `anyOf`, `oneOf`, `not`

JSON Schema's boolean-logic keywords require a value to satisfy multiple sub-schemas at once (`allOf`), at least one of several (`anyOf`), exactly one of several (`oneOf`), or specifically not satisfy one (`not`). JSSN represents these with dedicated operators rather than keywords.

## `&` — Intersection (allOf)

> **JSON Schema equivalent:** `allOf`

```jssn
address & {
  label?: str
}

defs <
  address = { street?: str }
>
```

Equivalent to:

```json
{
  "type": "object",
  "allOf": [{ "$ref": "#/$defs/address" }],
  "properties": {
    "label": { "type": "string" }
  },
  "$defs": {
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" }
      }
    }
  }
}
```

`&` chains for any number of schemas: `a & b & c` is equivalent to `allOf: [a, b, c]`.

### Closed Objects and `&`

> **JSON Schema equivalent:** `unevaluatedProperties`

An `obj` is closed by default (see [object.md](object.md)), so intersecting two closed shapes with `&` should reasonably close the result too — no property outside the union of both sides' properties should be allowed. In JSON Schema, this can't be expressed with `additionalProperties`, since a schema's own `additionalProperties` doesn't see properties introduced by `allOf`; `unevaluatedProperties` is the keyword that does.

This isn't confirmed yet, but the working assumption is:

- `address & { label?: str }` → `unevaluatedProperties: false`
- `address & { label?: str } & {...}` → `unevaluatedProperties: true` (the trailing bare `{...}` reopens it, same as it does for a plain `obj`)

## `|` — Union (anyOf)

> **JSON Schema equivalent:** `anyOf`

```jssn
circle | rectangle

defs <
  circle = { shape: "circle", radius: num }
  rectangle = { shape: "rectangle", width: num, height: num }
>
```

Equivalent to:

```json
{
  "anyOf": [{ "$ref": "#/$defs/circle" }, { "$ref": "#/$defs/rectangle" }],
  "$defs": {
    "circle": {
      "type": "object",
      "properties": {
        "shape": { "const": "circle" },
        "radius": { "type": "number" }
      },
      "required": ["shape", "radius"]
    },
    "rectangle": {
      "type": "object",
      "properties": {
        "shape": { "const": "rectangle" },
        "width": { "type": "number" },
        "height": { "type": "number" }
      },
      "required": ["shape", "width", "height"]
    }
  }
}
```

Like `&`, `|` chains for any number of schemas: `a | b | c | ...` is `anyOf: [a, b, c, ...]`.

## `~` — Negation (not)

> **JSON Schema equivalent:** `not`

```jssn
{
  username: str
  role: str & ~deprecatedRole
  team?: team
}

defs <
  deprecatedRole = enum("superadmin", "root", "godmode")
  team = { id: str, name?: str }
>
```

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "username": { "type": "string" },
    "role": {
      "allOf": [
        { "type": "string" },
        { "not": { "$ref": "#/$defs/deprecatedRole" } }
      ]
    },
    "team": { "$ref": "#/$defs/team" }
  },
  "required": ["username", "role"],
  "$defs": {
    "deprecatedRole": {
      "enum": ["superadmin", "root", "godmode"]
    },
    "team": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" }
      },
      "required": ["id"]
    }
  }
}
```

`~` is a unary prefix operator — it takes exactly one schema, so it never needs parens on its own.

## `^(...)` — Exactly One (oneOf)

> **JSON Schema equivalent:** `oneOf`

This one is rougher than the other three — worked out from a single example so far, not stress-tested.

```jssn
{
  value?: num
  next?: ^(#, null)
}
```

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "value": { "type": "number" },
    "next": {
      "oneOf": [{ "$ref": "#" }, { "type": "null" }]
    }
  }
}
```

Unlike `&`/`|`/`~`, `oneOf` is written as a call — `^(a, b, c)` for `oneOf: [a, b, c]` — rather than an infix operator.

## Combining Operators

Parentheses are required whenever `&` and `|` are mixed in the same expression — there's no defined precedence between them. `~` is exempt from this, since as a unary prefix operator it unambiguously binds to only the single schema right after it (see above).

```jssn
baseVariant & ~discontinuedVariant & (colorVariant | sizeVariant)
```

`(colorVariant | sizeVariant)` must be parenthesized here — `baseVariant & ~discontinuedVariant & colorVariant | sizeVariant` has no defined meaning.
