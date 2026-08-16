# Types

> **JSON Schema equivalent:** `prefixItems` (an array of schemas for positional/tuple validation), combined with `items: false` to disallow extra elements. In Draft 7 / 2019-09, the same thing is written as `items` given an array of schemas, with `additionalItems: false` instead of `items: false`.

## Type Names

JSON has six basic data types: `string`, `number`, `boolean`, `object`, `array`, and `null`.

JSON Schema reuses these terms as-is for its `type` keyword, and adds `integer` as a seventh type — a subtype of `number` used for validation.

JSSN mostly uses shorter aliases for these types, as shown below:

- `string` -> `str`
- `number` -> `num`
- `integer` -> `int`
- `boolean` -> `bool`
- `object` -> `obj`
- `array` -> `arr`
- `null` -> `null` (unchanged; already short)

### The `any` Type

In addition to the aliases above, JSSN has one more type: `any`. Unlike the others, `any` isn't one of JSON Schema's `type` values — it means no type constraint at all, equivalent to omitting `type` in JSON Schema (or using an empty schema, `{}`). A value of any type — including `null` — satisfies `any`.

```jssn
{
  data: any
}
```

#### Design Notes

- **A dedicated type, not an omitted one.** JSON Schema expresses "no constraint" by leaving `type` out entirely (or writing an empty schema, `{}`). JSSN instead gives it an explicit name, `any`, so every property or array slot keeps the same `key: type` / bare-type shape — no special-case grammar for "no type here."
- **Includes `null`.** Because `any` places no constraint at all, it also accepts `null` — this matches JSON Schema's empty-schema behavior, and differs from a future "any non-null type" union, should one be introduced.
- **Added for the required-without-properties edge case.** JSON Schema allows a key to be listed in `required` without appearing in `properties` at all, leaving its value unconstrained (see `required-optional-properties.md`). `any` exists to make that case expressible in JSSN — but it isn't limited to it; it works anywhere a type is expected, such as array elements or nested object properties.

## Usage

Two types, `arr` and `obj`, are compound types — they can contain other types inside them.
To write an `arr`, use brackets. If the `arr` has typed elements, simply list their types.
To write an `obj`, use braces. If the `obj` has properties, write the key name without quotes, followed by a colon (`:`) and the type.

On a single line, elements or properties are separated by a comma (`,`). Across multiple lines, a line break alone is enough to separate them.

#### Array

> **JSON Schema equivalent:** `prefixItems` (an array of schemas for positional/tuple validation), combined with `items: false` to disallow extra elements. In Draft 7 / 2019-09, the same thing is written as `items` given an array of schemas, with `additionalItems: false` instead of `items: false`.

```jssn
[int, bool, str]
```

or,

```jssn
[
  int
  bool
  str
]
```

#### Object

> **JSON Schema equivalent:** the `properties` keyword

```jssn
{
  one: int, two: int
}
```

or

```jssn
{
  one: int
  two: num
}
```

If an array or an object has no specified things inside of them, use `arr`, `obj` keyword, like other types.

```jssn
{
  hello: arr
  world: obj
}
```

Don't use empty `[]` or `{}` for this purpose — they look like, and in fact mean, an empty array or object.

```jssn
{
  hello: []
  world: {}
}
```

### Nested Array or Object

To write a nested array or object, use it as if it were a type — that is, write it wherever a type would normally go.

```jssn
[
  int
  {
    hello: str
    world: num
  }
]
```

```jssn
{
  title: str
  author: str
  content: [str, int, num]
}
```
