# Required and Optional Properties

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

## Required Without a Type Constraint

JSON Schema allows a key to appear in `required` without appearing in `properties` at all — the key must be present, but its value isn't constrained to any particular shape. In JSSN, this is written as a required property typed `any`.

```jssn
{
  id!: any
  name!: str
}
```

Here, `id` must be present but can hold any JSON value; `name` must be present and must be a string.

## Design Notes

- **Optional by default** matches JSON Schema's own default (properties are optional unless listed in `required`), rather than TypeScript's required-by-default convention.
- **Not `?` for optional.** Marking optional properties with `?` (required-by-default, like TypeScript) was considered, but rejected for now: it would flip the default away from JSON Schema's optional-by-default semantics, and it would use up `?`, which may be wanted later for a nullable-value shorthand (e.g. `str?` meaning "string or null").

## Out of Scope (For Now)

Relational/conditional requirements — e.g. "if property A is present, property B is required" (JSON Schema's `dependentRequired`, `dependentSchemas`, `if`/`then`/`else`) — are not covered here. These describe a relationship between properties rather than a property of a single key, so they will need their own construct rather than extending `!`.
