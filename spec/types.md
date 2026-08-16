# Types

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

## Usage

Two types, `arr` and `obj`, are compound types — they can contain other types inside them.
To write an `arr`, use brackets. If the `arr` has typed elements, simply list their types.
To write an `obj`, use braces. If the `obj` has properties, write the key name without quotes, followed by a colon (`:`) and the type.

On a single line, elements or properties are separated by a comma (`,`). Across multiple lines, a line break alone is enough to separate them.

#### Array

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
