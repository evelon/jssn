# References

> **JSON Schema equivalent:** the `$ref` keyword, together with `$defs` for named, reusable sub-schemas.

`$defs` holds named sub-schemas; `$ref` points to one from anywhere a schema is expected. JSSN drops the JSON Pointer syntax (`"#/$defs/name"`) in favor of shorter forms, and gives reusable schemas their own top-level block.

## Declaring Defs

Reusable schemas are declared in a `defs < ... >` block, separate from the schema body. Each entry is `name = type`. `$defs` doesn't interact with the other elements at its own level in JSON Schema — it's a namespace, not a sibling of `properties`/`required`, etc. — which is why it's always pulled out into its own block like this, rather than written as an ordinary property, regardless of where in the schema it lives.

```jssn
{
  billing_address: $address
}

defs <
  address = { street: str, city: str }
>
```

or if you want to emphasize that linkage between `defs` and the schema,

```jssn
{
  billing_address: $address
} defs <
  address = { street: str, city: str }
>
```

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "billing_address": { "$ref": "#/$defs/address" }
  },
  "required": ["billing_address"],
  "$defs": {
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" }
      },
      "required": ["street", "city"]
    }
  }
}
```

## Referencing a Def

Three forms exist, from most to least common.

### Nearest Reference

> **JSON Schema equivalent:** a `$ref` JSON Pointer resolved by hand to the nearest matching `$defs` entry

Write the def's name with a `$` prefix: `$address`. This searches outward from the current position for the nearest `defs` block containing that name — no need to count how many levels up it lives. If the same name exists at multiple levels (shadowing), the nearest one wins.

```jssn
{
  billing_address: $address
  shipping_address: $address
}

defs <
  address = { street: str }
>
```

### Absolute Path

> **JSON Schema equivalent:** `$ref: "#/$defs/..."`, abbreviated

Write `#`, then the path from the schema root, then `$name` for the final `$defs` lookup:

- `#$address` — a root-level def, equivalent to `#/$defs/address`
- `#order.customer$name` — a def scoped under `order.customer` (see [Defs Outside the Root](#defs-outside-the-root)); `/` between path segments becomes `.`, and only the final `$defs/name` segment keeps the `$` abbreviation

Use this when a nearest-reference could shadow the wrong def, or when being explicit about where a def lives matters more than brevity.

### Raw JSON Pointer

> **JSON Schema equivalent:** `$ref`, written out in full

The full, unabbreviated JSON Pointer also works, written without quotes: `#/$defs/address`. This is mostly useful for referencing something JSSN has no dedicated shorthand for — see [Referencing Outside `$defs`](#referencing-outside-defs).

## Common Patterns

### Referencing From `items`, `additionalProperties`, `patternProperties`

A def reference can appear anywhere a type can — including inside `array.md`'s and `object.md`'s own constructs, with no special syntax of its own.

```jssn
[...$product]

defs <
  product = { sku: str }
>
```

```jssn
{
  ...: $score
}

defs <
  score = num
>
```

```jssn
{
  /^env_/: $envValue
}

defs <
  envValue = str
>
```

These are equivalent to `items`, `additionalProperties`, and `patternProperties` each holding `{ "$ref": "#/$defs/..." }`.

### One Def Referencing Another

```jssn
{
  order: $order
}

defs <
  order = { customer: $person }
  person = { name: str }
>
```

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "order": { "$ref": "#/$defs/order" }
  },
  "required": ["order"],
  "$defs": {
    "order": {
      "type": "object",
      "properties": {
        "customer": { "$ref": "#/$defs/person" }
      },
      "required": ["customer"]
    },
    "person": {
      "type": "object",
      "properties": {
        "name": { "type": "string" }
      },
      "required": ["name"]
    }
  }
}
```

An indirection chain (`a = b`, `b = c`, `c = { ... }`) works the same way — each `$name` resolves independently, so nothing beyond the forms above is needed to write one.

### Self-Reference (Recursive Structures)

A def can reference itself, for structures with unbounded nesting:

```jssn
$node

defs <
  node = {
    value: str
    children: [...$node]
  }
>
```

Equivalent to:

```json
{
  "$ref": "#/$defs/node",
  "$defs": {
    "node": {
      "type": "object",
      "properties": {
        "value": { "type": "string" },
        "children": {
          "type": "array",
          "items": { "$ref": "#/$defs/node" }
        }
      },
      "required": ["value", "children"]
    }
  }
}
```

### Root Reference (`#`)

A bare `#` refers to the whole document — useful when the recursive shape _is_ the root schema, with no separate `$defs` entry needed. See [boolean-logic.md](boolean-logic.md)'s `oneOf` section for a worked example (a linked-list node whose `next` is either another node or `null`, via `next: ^(#, null)`).

### Mutually Recursive Defs

```jssn
$expr

defs <
  expr = num | $binaryOp
  binaryOp = {
    op: enum("+", "-", "*", "/")
    left: $expr
    right: $expr
  }
>
```

Equivalent to:

```json
{
  "$ref": "#/$defs/expr",
  "$defs": {
    "expr": {
      "oneOf": [{ "type": "number" }, { "$ref": "#/$defs/binaryOp" }]
    },
    "binaryOp": {
      "type": "object",
      "properties": {
        "op": { "enum": ["+", "-", "*", "/"] },
        "left": { "$ref": "#/$defs/expr" },
        "right": { "$ref": "#/$defs/expr" }
      },
      "required": ["op", "left", "right"]
    }
  }
}
```

The absolute form (`left: #$expr`) works here too, and reads the same regardless of how deep `binaryOp` is nested — the nearest-reference form only has an advantage when the exact depth would otherwise need to be counted, which doesn't come up here.

### Recursive General-Purpose Value Type

The pattern `$defs`/`$ref` gets used for most often in practice: "any value expressible in JSON."

```jssn
$json

defs <
  json = str | num | bool | null | [...$json] | { ...: $json }
>
```

Equivalent to:

```json
{
  "$ref": "#/$defs/json",
  "$defs": {
    "json": {
      "oneOf": [
        { "type": "string" },
        { "type": "number" },
        { "type": "boolean" },
        { "type": "null" },
        { "type": "array", "items": { "$ref": "#/$defs/json" } },
        {
          "type": "object",
          "additionalProperties": { "$ref": "#/$defs/json" }
        }
      ]
    }
  }
}
```

Nothing new is needed here — array.md's `[...type]`, object.md's `{...: type}`, and boolean-logic.md's `|` all combine with a self-reference exactly as they would with any other type.

## Uncommon Forms

The forms below are legal but rarely needed. Most readers can skip this section.

### `$anchor`

> **JSON Schema equivalent:** `$anchor`, referenced as `$ref: "#name"`

Referencing by a plain name instead of a path — mainly useful when a schema is meant to be referenced from other documents.

```jssn
{
  billing_address: #address
}

defs <
  address as #address = { street: str }
>
```

### Referencing Outside `$defs`

> **JSON Schema equivalent:** `$ref` pointed at a non-`$defs` location

`$ref` can target any schema in the document, not just something under `$defs`. JSSN has no dedicated notation for this — it's treated as an anti-pattern, and falls back to a raw JSON Pointer:

```jssn
{
  primary_email: str(email)
  backup_email: #/properties/primary_email
}
```

### Defs Outside the Root

> **JSON Schema equivalent:** `$defs` nested inside a property's own schema, rather than at the document root

The same reasoning from [Declaring Defs](#declaring-defs) applies here too — `$defs` is a namespace regardless of where it lives, so it's still pulled out into its own block, just path-qualified to say which property it belongs to:

```jssn
{
  order: { item: $lineItem }
}

order.defs <
  lineItem = { sku: str }
>
```

Equivalent to:

```json
{
  "type": "object",
  "properties": {
    "order": {
      "type": "object",
      "properties": {
        "item": { "$ref": "#/properties/order/$defs/lineItem" }
      },
      "required": ["item"],
      "$defs": {
        "lineItem": {
          "type": "object",
          "properties": {
            "sku": { "type": "string" }
          },
          "required": ["sku"]
        }
      }
    }
  },
  "required": ["order"]
}
```

### A Def That Is a Boolean Schema

> **JSON Schema equivalent:** a `$defs` entry whose value is `true` or `false`

```jssn
{
  metadata: $unconstrained
  locked_field: $nothingAllowed
}

defs <
  unconstrained = true
  nothingAllowed = false
>
```

The indirection buys nothing here — `metadata: true` and `locked_field: false` mean exactly the same thing without going through a def at all. This section exists to show the notation is legal, not because it's useful.

## Design Notes

- **Nearest reference over relative paths.** Two earlier designs counted levels explicitly, mirroring relative file paths: incrementing dots (`.`, `..`, `...` for 0, 1, 2 levels up) and, separately, repeating a segment Unix-style (`../..`). Both were dropped: the count had to be re-derived from the surrounding structure every time, which cost more in practice than the shorter spelling saved. Nearest-match reference removes the counting entirely, at the cost of shadowing being implicit rather than visible at the reference site — considered an acceptable trade, since two defs sharing a name at different levels is rare and always resolvable with an absolute path.

## Out of Scope (For Now)

- `$dynamicRef`/`$dynamicAnchor` — a mechanism for a def that a *referencing* schema can override, meant for extensible base-schema designs (schema libraries, vocabularies). Belongs in this document once designed, but no notation is settled on yet, so none is written here.
