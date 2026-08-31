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
  "required": ["name", "email", "age"],
  "additionalProperties": false
}
```

## Required and Optional Properties

> **JSON Schema equivalent:** the `required` array, combined with `properties`

Properties are required by default. To mark a property as optional, append `?` to its key name, immediately before the colon.

```jssn
{
  name: str
  email: str
  age?: int
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

The `?` always goes right after the key name — not before it, and not after the type.

```jssn
age?: int
```

not

```jssn
?age: int
```

or

```jssn
age: int?
```

## Nested Objects

Each `obj`, at any depth, has its own independent set of required/optional properties. Marking a property `?` only affects whether it is optional within its immediate parent object.

```jssn
{
  title: str
  meta?: {
    tags: arr
    notes?: str
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

JSON Schema allows a key to appear in `required` without appearing in `properties` at all — the key must be present, but its value isn't constrained to any particular shape. In JSSN, a bare key (no colon, no type) already means "required, typed `any`" — see [types.md](types.md) for the bare-key `any` shorthand — so this case needs no extra marker at all.

```jssn
{
  id
  name: str
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

The same combination works the other way too: `id?` (bare key, `?` suffix) is optional and typed `any`.

## Design Notes

- **Required by default, inverting JSON Schema's own default.** JSON Schema treats a property as optional unless it's listed in `required`. JSSN flips this so that omitting a marker means required. This keeps required/optional consistent with the two other places JSSN already flips JSON Schema's default from open to closed — array items (see [array.md](array.md)) and `additionalProperties` (see below) — both of which are unconstrained/open by default in JSON Schema but closed by default in JSSN. Leaving `required` as the odd one out, still following JSON Schema's optional-by-default convention, would have made JSSN internally inconsistent about what "no marker" means.
- **`?` for optional, not `!` for required.** An earlier version of this spec used `!` to mark a property required, optional by default (matching JSON Schema's own default, see above). In practice, forgetting to mark a property required (a missing `!`) is a much easier mistake to make — and a much easier one to miss, since the unmarked property looks identical to any other optional property — than mismarking a property that should be optional. Marking optional properties with `?` instead means the common mistake (forgetting to mark a property optional) produces a property that looks the same as every other required property, and the rarer, more consequential mistake (a property that's accidentally optional) is visible immediately as a stray `?`. This also uses `?` for a purpose closer to its meaning in TypeScript and similar languages, where `?` marks optionality rather than requiredness.
- **Spends the `?` glyph the earlier design reserved for nullability.** The `!`-based design considered and rejected `?` for optionality specifically to keep it free for a possible nullable-value shorthand later (e.g. `str?` meaning "string or null"), since a single glyph can't cleanly carry both meanings if used the same way in both spots. This version accepts that trade-off: `?` after a *key* now means optional, so a future nullable shorthand would need a different marker, or would need to reuse `?` after a *type* instead and rely on position (key vs. type) to disambiguate. Given how much more common the required/optional mistake is than the need for a nullable shorthand (still unscheduled — see the roadmap in [README.md](../README.md)), this is judged worth it.

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
  },
  "required": ["name", "email", "age"]
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
  "required": ["name", "email", "age"],
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
  },
  "required": ["name", "email", "age"]
}
```

## Out of Scope (For Now)

- `propertyNames` may go between the size and the obj body (`{}`). The details are still undecided.
- Relational/conditional requirements — e.g. "if property A is present, property B is required" (JSON Schema's `dependentRequired`, `dependentSchemas`, `if`/`then`/`else`) — are not covered here. These describe a relationship between properties rather than a property of a single key, so they will need their own construct rather than extending `?`.
