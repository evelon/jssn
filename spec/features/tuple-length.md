# Tuple Length

> **JSON Schema equivalent:** `items`, `prefixItems`, `minItems`, `maxItems`. In Draft 7 / 2019-09, `prefixItems` doesn't exist — `items` takes an array of schemas instead, and `additionalItems` takes over the trailing-elements role that `items` plays here (`minItems`/`maxItems` are unchanged).

## Closed Tuples

A tuple of fixed length is written by simply listing its element types:

```jssn
[bool, str, int]
```

or

```jssn
[
  bool
  str
  int
]
```

This is equivalent to:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "items": false
}
```

## Open Tuples

A tuple that stays open to further elements of a given type, past its fixed prefix, is written with `...` immediately before that type. The example below is open to `num` past its first three elements:

```jssn
[bool, str, int, ...num]
```

Equivalent to:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "items": {
    "type": "number"
  }
}
```

A tuple open to any type past its prefix is written with a bare `...`:

```jssn
[bool, str, int, ...]
```

This is the `any`-omission form of:

```jssn
[bool, str, int, ...any]
```

which is equivalent to:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "items": true
}
```

## Bounded Trailing Elements

Past a tuple's fixed prefix, the allowed count of trailing elements of a given type is written `(min)..(max) (type)` — a single space separates the count from the type. For example, "between 2 and 4 more `num`s" is `2..4 num`; "3 or more" is `3.. num`; "up to 4" is `..4 num`. `any` can be dropped from this position, so `2..4`, `3..`, and `..4` are equally valid.

This bounded-count notation is a separate token from `...`. By the rule above, an unbounded trailing count (no minimum, no maximum) would be written `.. (type)` — but it's written `...(type)` instead, reusing the fully-open notation from the previous section. This exception is purely for readability: `...num` reads better than `..num`.

### Optionally-Present Elements

A tuple can have a variable length while still fixing the type at each index. In the example below, index 0 (`bool`) must always be present; if the array grows, index 1 must be `str` and index 2 must be `int`, but the length can never exceed 3. The boundary between the required and optional portions is marked with `;`; a `,` is never used at that same boundary.

```jssn
[bool; str, int]
```

or

```jssn
[
  bool;
  str
  int
]
```

Equivalent to:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 1,
  "items": false
}
```

### Minimum-Bounded Trailing Elements

An open tuple can require a minimum count of trailing elements.

```jssn
[bool, str, int, 2..]
```

or

```jssn
[bool, str, int, 2.. any]
```

Equivalent to:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 5
}
```

With a type:

```jssn
[bool, str, int, 2.. num]
```

or

```jssn
[
  bool
  str
  int
  2.. num
]
```

Equivalent to:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 5,
  "items": { "type": "number" }
}
```

### Maximum-Bounded Trailing Elements

An open tuple can also cap the count of trailing elements. The example below is open, but at most 3 further elements may follow.

```jssn
[bool, str, int, ..3]
```

or

```jssn
[
  bool
  str
  int
  ..3
]
```

Equivalent to:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "maxItems": 6
}
```

### Min/Max-Bounded Trailing Elements

Both a minimum and a maximum count of trailing elements can be given together.

```jssn
[bool, str, int, 2..5]
```

Equivalent to:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 5,
  "maxItems": 8
}
```

### Extending by Exactly One Element

When `minItems` and `maxItems` are equal, and exactly one greater than `prefixItems`'s length, the tuple behaves as if `prefixItems` had simply been extended by one element — semantically identical to a closed tuple.

This isn't new syntax. Once `minItems` and `maxItems` both equal `prefixItems`'s length, no array index can ever reach the position `items` would apply to — so `items: false`, `items: { ... }`, and `items: true` all behave identically. The two schemas below are therefore equivalent to the `items: false` form already covered under Closed Tuples, and are written the same way, with no extra punctuation. This section exists only to show that these differently-shaped (and somewhat awkwardly-written) schemas fold back into a closed tuple.

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 4,
  "maxItems": 4,
  "items": { "type": "number" }
}
```

```jssn
[bool, str, int, num]
```

or

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "minItems": 4,
  "maxItems": 4,
  "items": true
}
```

```jssn
[bool, str, int, any]
```

> `any` must be written out explicitly here — this is a tuple slot, and `any`-omission doesn't apply inside a tuple (see [types.md](types.md)).

## Uncommon Tuples

The sections below cover results that are rarely intended. Most readers can skip this section.

JSON Schema only requires `minItems` and `maxItems` to be non-negative integers — either is valid on its own. But combined with each other, or with `prefixItems`/`items`, some combinations describe a tuple whose shape doesn't make sense.

Rather than silently rendering only the valid portion, jssn surfaces these combinations using `;;`, to warn the author that the source JSON Schema was likely written by mistake. Wherever a part of the tuple is invalid, its type is prefixed with `-` for readability.

If a jssn tuple contains `;;`, its source JSON Schema is probably a mistake.

### Unreachable Elements

`prefixItems` may declare types for indices that the tuple's length can never reach.

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" }
  ],
  "maxItems": 2
}
```

Here, index 2 is typed `integer`, but `maxItems: 2` makes that meaningless. jssn marks this with `;;`, to show that the effective length is 2 and everything past it is discarded. The `,` that would normally precede it is dropped.

```jssn
[bool, str;; -int]
```

or

```jssn
[
  bool
  str;;
  -int
]
```

`;;` reuses the same character as the `;` from Optionally-Present Elements, which can be confusing. The following JSON Schema makes the resulting notation easier to predict:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 1,
  "maxItems": 3
}
```

jssn writes this as:

```jssn
[bool; str, int;; -int]
```

or

```jssn
[
  bool;
  str
  int;;
  -int
]
```

When `minItems` and `maxItems` are equal, and `prefixItems` is longer than both:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 2,
  "maxItems": 2
}
```

jssn drops the `;` that `minItems` would otherwise produce, since it would land on the exact same position as `;;`:

```jssn
[bool, str;; -int, -int]
```

or

```jssn
[
  bool
  str;;
  -int
  -int
]
```

### Inside-Out Tuples

Consider `minItems` greater than `maxItems`: no array can ever satisfy such a schema. jssn still uses a notation richer than a plain `[]`, though, so the shape of the original mistake stays visible.

`;` sits at the position `minItems` points to, and `;;` sits at the position `maxItems` points to — the same rule as in Unreachable Elements. There, `minItems <= maxItems` put `;` before `;;`; here, `minItems > maxItems` by definition, so the two markers are placed in order of value and `;;` always comes first. And because no array can satisfy this tuple at all, every element and token gets a `-` prefix — including the elements before `;;`, unlike in Unreachable Elements, where that leading portion was still reachable.

When `minItems` points past the end of `prefixItems`, that excess isn't a real `prefixItems` element — it's a virtual slot, so it reuses the open-tuple notation: a single excess slot is written as a bare type (or `any`), just like Extending by Exactly One Element; two or more excess slots reuse the `(count)..` notation from Minimum-Bounded Trailing Elements (with no type after it, since none is given). Whenever `;` lands on the very last position in the notation, nothing follows it — it appears as a trailing `;`.

Take an example where both values are smaller than `prefixItems`'s length:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 3,
  "maxItems": 2
}
```

`minItems` is 1 greater than `maxItems`. This is written as:

```jssn
[-bool, -str;; -int; -int]
```

`;;` lands where `maxItems` (2) points — after the second element — and `;` lands where `minItems` (3) points — after the third. `;;` comes before `;`, and since no index here exceeds `prefixItems`'s length (4), no virtual slot is needed.

Now take an example where `minItems` is 1 greater than `prefixItems`'s length, while `maxItems` stays smaller:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 5,
  "maxItems": 2
}
```

```jssn
[-bool, -str;; -int, -int, -any;]
```

`minItems` (5) is 1 greater than `prefixItems`'s length (4), so — just as in Extending by Exactly One Element — the one excess slot is appended as a bare type with no `(count)..` notation. `items` isn't specified, so the type is `any`; since the schema is unsatisfiable, it gets a `-`. `minItems`'s position coincides with the very end of the notation, so `;` trails after `-any`.

When `minItems` is 2 or more past `prefixItems`'s length:

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "boolean" },
    { "type": "string" },
    { "type": "integer" },
    { "type": "integer" }
  ],
  "minItems": 7,
  "maxItems": 1
}
```

```jssn
[-bool;; -str, -int, -int, -3..;]
```

`minItems` (7) is 3 past `prefixItems`'s length (4), so with two or more excess slots, this reuses the `(count)..` notation from Minimum-Bounded Trailing Elements as `3..`, with a `-` prefix. Here too, `minItems`'s position coincides with the end of the notation, so `;` trails at the end.
