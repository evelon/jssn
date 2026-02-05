# JSSN (JSON Schema Symbolized Notation)

## JSSN Specification — Draft v0.1

> v0.1 defines the core JSSN language only.  
> Module systems, multi-file composition, and advanced tooling semantics are intentionally out of scope.

> Pronunciation: "jay-es-son" (J-S-S-N)

> Status: Draft
> Scope: This document specifies the **format** of JSSN.
> Parsing, runtime validation behavior, and tooling are explicitly out of scope.

---

## 0. Notation Conventions

This document uses small pieces of **emission pseudocode** when describing JSON Schema mappings.

- `schema(X)` denotes **the JSON Schema produced by emitting** the JSSN type expression `X`.
- `schema(X)` is **specification shorthand** and is **NOT** literal JSON Schema syntax.

Example:

- `propertyNames: schema(str(1..5))`

means that tooling emits:

```json
{
  "propertyNames": {
    "type": "string",
    "minLength": 1,
    "maxLength": 5
  }
}
```

### 0.1 JSON Schema Target

Unless otherwise noted, the JSON Schema emission described in this document targets **JSON Schema 2020-12**. This matters for tuple/array keywords such as `prefixItems`.

## 1. Design Principles

- JSSN is a **schema-first DSL** designed for humans.
- JSSN is a **source format** that can be transformed into JSON Schema.
- JSSN separates the following concerns explicitly:
  - **type** (data kind)
  - **constraint** (range, length, size)
  - **format** (semantic hint such as uuid, email, date-time)
  - **metadata** (documentation, ownership, stability)
- Every construct in JSSN MUST be either:
  - directly representable in JSON Schema, or
  - reducible to a JSON Schema–representable construct via desugaring.

### 1.1 Design Intent (Non-normative)

The following notes clarify **why** certain design decisions exist.  
These notes are non-normative and do not change validation semantics.

- JSSN is intended to be a **human-authored source language** for JSON Schema.
- JSON Schema is treated as a compilation target; JSSN is the authoring format.
- The specification prioritizes:
  - readability,
  - diff stability,
  - deterministic emission,
  - and long-term maintainability of schema documents.
- JSSN intentionally avoids introducing constructs that cannot be faithfully emitted as JSON Schema.
- Where JSON Schema provides multiple equivalent encodings, JSSN selects a canonical representation to reduce ambiguity.

---

## 2. Document Structure

A JSSN document consists of top-level blocks.

### 2.1 Top-level Blocks

Allowed blocks:

- `meta { ... }` — require, one
- `type { ... }` — optional, at most one
- `schema <Name> { ... }` — required, one or more

Example:

```jssn
meta { ... }

type { ... }

schema ExampleSchema { ... }
schema AnotherSchema { ... }
```

### 2.2 Canonical Block Order

When normalized, blocks MUST appear in this order:

1. `meta` (one)
2. `type`
3. `schema` (one or more)

### 2.3 Separators: Line Break and Comma

JSSN treats **line breaks** as the primary separator in multi-line constructs.

- In multi-line objects and arrays, **a line break separates entries**.
- Commas are only meaningful when writing a construct on a **single line**.
- If a comma appears immediately before a line break, it MUST be ignored.

Examples (equivalent):

```jssn
[
  int
  str
]
```

```jssn
[
  int,
  str,
]
```

```jssn
[int, str]
```

---

## 3. Meta Block

### 3.1 Purpose

The `meta` block contains **document-level metadata**.

- It does not define data structure.
- It does not affect schema semantics.
- It is intended for humans and tooling.

### 3.2 Syntax

```jssn
meta {
  jssn_version: "0.1"
  title: "Example"
  description: "..."
}
```

### 3.3 Standard Keys (non-exhaustive)

- `jssn_version`
- `title`
- `description`
- `package` / `namespace`
- `entry` (default schema name)
- `stability` (draft | stable | deprecated)

Additional keys MAY be present.

### 3.4 Required Keys (Normative)

- `jssn_version` MUST be present.
- If a document contains more than one `schema` block, `entry` MUST be present and MUST equal the name of one declared `schema`.
- If a document contains exactly one `schema` block and `entry` is absent, tooling MUST treat that schema as the entry schema.

---

## 4. Type Block

### 4.1 Purpose

The `type` block defines **named reusable types**.

JSSN supports two declaration modes inside `type { ... }`:

- **Defined types (emit to `$defs`)** — declared with `=`
- **Named inline types (inline-expand)** — declared with `^=`

The inline/defs decision is made **only at declaration time** and MUST NOT be changed at usage sites.

All named identifiers in a JSSN document share a single global namespace:

- defined type names (`Name = ...`)
- named inline type names (`Name ^= ...`)
- schema names (`schema Name { ... }`)

These base identifiers MUST be globally unique. If two declarations resolve to the same identifier string, the document is invalid.

---

### 4.2 Declaration Forms

#### 4.2.1 Defined Type (Emits to `$defs`)

A defined type produces a JSON Schema `$defs` entry.

```jssn
type {
  SeatNo = int(0..7)
  Status = str(enum RUNNING|ENDED)
}
```

Rules:

- `Name = Expr` declares a **defined type**.
- Tooling MUST emit a JSON Schema definition under `$defs.Name`.
- Every usage of `Name` MUST emit a `$ref` to that `$defs` entry.
- Tooling MUST NOT inline-expand a defined type.

Usage:

```jssn
seat_no: SeatNo
```

Emits:

```json
{ "$ref": "#/$defs/SeatNo" }
```

---

#### 4.2.2 Named Inline Type (Always Inline)

A named inline type is declared using `^=`.

```jssn
type {
  DieResult ^= int(1..6)
}
```

Rules:

- `Name ^= Expr` declares a **named inline type**.
- Named inline types MUST NOT generate `$defs` entries.
- Every usage of `Name` MUST inline-expand `Expr` at the usage site.
- Tooling MUST NOT emit `$ref` for named inline types.

Example:

```jssn
type {
  DieResult ^= int(1..6)
}

schema Test {
  cast_result: DieResult
}
```

Emitted JSON Schema (conceptual):

```json
{
  "type": "object",
  "properties": {
    "cast_result": {
      "type": "integer",
      "minimum": 1,
      "maximum": 6
    }
  },
  "required": ["cast_result"],
  "additionalProperties": false
}
```

---

### 4.3 Usage Rules

Usage syntax does NOT encode inline vs defs behavior.

```jssn
field: Name
```

Resolution rules:

- If `Name` is declared as a defined type (`Name = ...`) → emit `$ref`.
- If `Name` is declared as a named inline type (`Name ^= ...`) → inline-expand.

This ensures that inline/defs policy is defined only once and users do not need to think about it at usage sites.

---

### 4.4 Format Alias

A **format alias** is a convenience name for a JSON Schema `format` applied to `str`. Format aliases MAY be declared as either defined types (`=`) or named inline types (`^=`).

```jssn
type {
  uuid = str(uuid)
  email ^= str(email)
  short_email = str(email, 5..30)
}
```

Rules:

- A format alias MUST have the RHS form `str(<format>)` or `str(<format>, <range>)`.
- A format alias MAY be declared using either `=` or `^=`.
- If declared with `=`, the alias is a defined type and tooling MUST emit `$defs.<Name>` and `$ref` on use.
- If declared with `^=`, the alias is a named inline type and tooling MUST inline-expand on use.
- Annotations follow the declaration mode:
  - `Name = str(...)` MAY carry type-level annotations.
  - `Name ^= str(...)` MUST NOT carry annotations.

Usage:

```jssn
id: uuid
contact: email
```

Tooling MUST apply the declaration mode: defined format aliases emit `$ref`; inline format aliases inline-expand into the corresponding `str(...)` form.

---

### 4.5 Type-level Annotation Rules

Annotations MAY appear on **defined type** declarations.

```jssn
type {
  Status = str(enum RUNNING|ENDED) @note("status enum")
}
```

Rules:

- Type-level annotations are allowed only on **defined types** (`Name = Expr`).
- Named inline types (`Name ^= Expr`) MUST NOT carry annotations.
- Type annotations map to JSON Schema keywords inside `$defs.<Name>`.

Allowed mappings:

- `@note("text")` → `description`
- `@example(<literal>)` → `examples` (array)
- `@deprecated` → `deprecated: true`

Named inline types do not produce standalone schema nodes and therefore cannot carry annotations.

## 5. Schema Block

### 5.1 Purpose

A `schema` block defines exactly one **root object schema**.

```jssn
schema CaseSnapshot {
  ...
}
```

### 5.2 Rules

- Named identifiers MUST be globally unique within the document (see §4.1): schema names, defined type names (`Name = ...`), and named inline type names (`Name ^= ...`) share a single namespace.
- Schema blocks define object structure only.
- Type declarations are NOT allowed inside schema blocks.

### 5.3 Schema References (New)

Schemas MAY be referenced as types from within other schemas.

Example:

```jssn
schema Player {
  seat_no: int(0..7)
}

schema CaseSnapshot {
  players: [Player...]
}
```

Mapping intention:

- Each `schema <Name> { ... }` is emitted as a named schema definition (e.g., under JSON Schema `$defs`).
- References to `<Name>` are emitted as `$ref` to that definition.

Notes:

- Recursive and mutually recursive schema references are allowed and map to JSON Schema `$ref`.
- The document MAY designate a single entry schema via `meta.entry`.
- If a document contains more than one `schema` block, `meta.entry` is REQUIRED (see §3.4).

Emission note (normative): Tooling MUST emit all `schema <Name> { ... }` blocks as named definitions under JSON Schema `$defs`. The entry schema (determined by §3.4) MUST be emitted as a top-level `$ref` to `#/$defs/<EntryName>`.

---

## 6. Type System

### 6.1 Primitive Types (Keywords)

The following are reserved primitive type keywords:

- `int` → integer
- `num` → number
- `str` → string
- `bool` → boolean
- `null` → null
- `obj` → object
- `arr` → array

These keywords MAY NOT be redefined as aliases.

To avoid confusion with JSON Schema terminology, the following identifier strings are **forbidden** as user-defined names (they are not keywords, but documents using them as schema/type names are invalid):

- `integer`
- `number`
- `string`
- `boolean`
- `object`
- `array`

Tooling MUST treat these forbidden identifiers case-insensitively.

---

## 6.2 Object and Array Types

### Object

```jssn
{
  field: Type
}
```

### Object — Header Entries (New)

An object MAY start with **header entries** that apply to multiple properties.

Header entry kinds:

- `*` (global rule): applies to **all** properties in the object
- `/regex/` (pattern rule): applies to properties whose names match the regex

Header entries are representable in JSON Schema via `propertyNames` and `patternProperties`.

#### Avoiding Confusion: `/regex/: V` vs `...(/regex/): V`

Both forms use `/.../`, but they constrain different things:

| JSSN form         | Meaning                                                                                    | JSON Schema keyword                      |
| ----------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------- |
| `/regex/: V`      | Constrains the **values** of properties whose names match `regex`                          | `patternProperties`                      |
| `...(/regex/): V` | Constrains **property names** (keys) using `regex` and constrains additional values to `V` | `propertyNames` + `additionalProperties` |

Example:

```jssn
{
  /^i-/: int
  ...: str
}
```

Means: keys starting with `i-` must have integer values; all other additional keys must have string values.

#### Global Rule Entry (`*`)

Syntax:

```jssn
*: V
*(1..5): V
```

Semantics:

- `*: V` means **all values** in the object MUST satisfy `V`.
- `*(1..5): V` additionally constrains **all key names** to length `1..5`.

JSON Schema mapping intention:

- Value rule: emitted as the base value schema for the object (see §7.2.4 for interaction with other entries)
- Key length rule: emitted as `propertyNames: schema(str(1..5))`

Restrictions:

- An object MUST contain at most one `*` entry.

#### Pattern Rule Entry (`/regex/`)

Syntax:

```jssn
/^i-/: V
```

Semantics:

- Applies to properties whose names match the regex; those property values MUST satisfy `V`.

JSON Schema mapping intention:

- Emitted as `patternProperties: { "^i-": schema(V) }`.

Notes:

- Regex is evaluated using JSON Schema regex semantics; tooling MUST strip surrounding slashes when emitting JSON Schema.

### Object — Dict / Map Sugar (Spread Form)

Objects are **closed by default** (see §7.1), but a schema MAY allow additional (unknown) keys using the spread form.

#### Mixed Fixed Fields + Additional Keys (Allowed)

The spread form MAY be combined with fixed fields to allow a partially open object.

```jssn
{
  id: str
  flags?: [str...]
  ...
}
```

Mapping intention (JSON Schema):

- `properties` contains the fixed fields
- `required` contains all non-optional fixed fields
- `additionalProperties: {}` (because `any`)

#### Allowing Additional Keys (Dictionary)

Mapping intention (JSON Schema):

- `additionalProperties: schema(V)`

`any` MAY be used to allow any value type:

```jssn
{
  ...: any
}
```

Shorthand: `...` is equivalent to `...: any`.

```jssn
{
  ...
}
```

Mapping intention:

- `additionalProperties: {}`

---

#### Constraining Key Names

Since JSON object keys are strings, key constraints are expressed using string constraints.

Length-constrained spread keys MAY be written using either range syntax or keyed syntax. Canonical output MUST use the range shorthand form.

```jssn
{
  ...(1..20): V
}
```

Keyed syntax is also allowed:

```jssn
{
  ...(min=1, max=20): V
}
```

Open-ended forms are allowed:

```jssn
{
  ...(min=1): V
}

{
  ...(max=20): V
}
```

Canonicalization rules:

- `...(min=1, max=20)` → `...(1..20)`
- `...(min=1)` → `...(1..)`
- `...(max=20)` → `...(..20)`

Mapping intention:

- `propertyNames: schema(str(1..20))`
- `additionalProperties: schema(V)`

Notes:

- The explicit form `...str(1..20): V` remains NOT allowed in JSSN v0.1.

---

#### Format-Constrained Keys (New)

A format identifier MAY be used to constrain key names:

```jssn
{
  ...(uuid): V
}
```

Mapping intention:

- `propertyNames: schema(str(uuid))`
- `additionalProperties: schema(V)`

Warning:

- This uses JSON Schema `format`, which may be treated as a semantic hint by some validators. Tooling SHOULD document validator behavior and users SHOULD NOT rely on `format` for strict security validation.

---

#### Pattern-Constrained Keys

A regular expression MAY be used to constrain key names:

```jssn
{
  ...(/pattern/): V
}
```

Mapping intention:

- `propertyNames: { type: "string", pattern: "pattern" }`
- `additionalProperties: schema(V)`

Notes:

- The tail `/.../` is JSSN syntax; JSON Schema expects the pattern as a string. Tooling MUST strip the surrounding slashes when emitting JSON Schema.
- Tooling MUST NOT add, remove, or rewrite anchors; the emitted `pattern` string MUST equal the regex text as written inside `/.../`.
- JSON Schema `pattern` performs partial matches. If full-string matching is desired, authors SHOULD add anchors (e.g., `^...$`) explicitly.
- Regex flags (e.g., `/abc/i`) are NOT representable in standard JSON Schema `pattern` and are therefore NOT allowed in JSSN v0.1.
- The `/.../` pattern literal is opaque and MUST be preserved byte-for-byte; tooling MUST only strip the surrounding slashes when emitting JSON Schema.

### Array

JSSN distinguishes **homogeneous arrays** from **tuple-shaped arrays**.

#### Homogeneous Arrays

Homogeneous arrays are written using the `T...` suffix inside brackets:

```jssn
[T...]
```

Semantics:

- All items MUST satisfy `T`.

Mapping intention (JSON Schema):

- `items: schema(T)`

#### Tuple-Shaped Arrays (Tuples)

Tuples specify per-position item types.

##### Strict Tuples (Default)

```jssn
[T1, T2, T3]
```

Semantics:

- The array MUST have exactly 3 items.
- Item `i` MUST satisfy `Ti`.
- No additional items are allowed.

Mapping intention (JSON Schema 2020-12):

- `prefixItems: [schema(T1), schema(T2), schema(T3)]`
- `items: false`
- `minItems = maxItems = 3`

##### Open Tuples (Any Tail)

Open tuples allow additional items of unspecified type.

Canonical shorthand:

```jssn
[T1, T2, ...]
```

This is equivalent to:

```jssn
[T1, T2, any...]
```

Semantics:

- The array MUST have at least 2 items.
- The first items MUST satisfy `T1`, `T2`.
- Additional items MAY be any JSON value.

Mapping intention (JSON Schema 2020-12):

- `prefixItems: [schema(T1), schema(T2)]`
- `items: {}`
- `minItems = 2`

##### Tail-Repeating Tuples

Tuples MAY specify a repeating tail item type.

```jssn
[T1, T2, T...]
```

Semantics:

- The array MUST have at least 2 items.
- The first items MUST satisfy `T1`, `T2`.
- Additional items MUST satisfy `T`.

Mapping intention (JSON Schema 2020-12):

- `prefixItems: [schema(T1), schema(T2)]`
- `items: schema(T)`
- `minItems = 2`

If the tail type is a union, it MUST be parenthesized:

```jssn
[T1, T2, (A | B)...]
```

##### Note: `[T, ...]` vs `[T...]`

- `[T, ...]` is an **open tuple** with a required first item `T` and an `any` tail.
- `[T...]` is a **homogeneous array** where every item must satisfy `T`.

#### Array Length Constraints

Array length constraints MAY be written either as a postfix on the array expression or as a prefix range.

Allowed forms (equivalent):

```jssn
[T...](1..3)
```

```jssn
(1..3)[T...]
```

The single-number shorthand is allowed:

```jssn
[T...](3)
```

```jssn
(3)[T...]
```

Mapping intention (JSON Schema):

- `(min..max)` maps to `minItems` / `maxItems`.
- `(n)` maps to `minItems = maxItems = n`.

Notes:

- Length constraints apply to both homogeneous arrays and tuples.
- Canonicalization rules for array length constraints are defined in §8.4.

---

## 6.3 Enum

### 6.3.1 Enum Block Syntax (Type Block Only)

Enums MAY be declared as reusable types inside the `type` block using a block form.

```jssn
type {
  VoteKind = enum: str {
    FIRST_VOTE
    "SECOND VOTE"
    "INTERRUPTED"
  }
}
```

Rules:

- Enum block syntax is allowed ONLY inside the `type` block.
- Enum blocks MUST NOT appear inline inside `schema` fields.
- The declared enum becomes a named type alias and may be referenced like any other type.
- The base type (`str`, `int`, etc.) determines the JSON Schema type.
- Enum elements represent literal JSON values and are emitted as JSON Schema `enum`.
- Inline enum syntax (e.g., `str(enum ...)`) MUST NOT be used inside `type { ... }`. Use enum blocks instead.
- Canonicalization: If an enum block contains exactly one element, canonical output MUST replace the enum block with a literal type alias (see §6.10).

### 6.3.2 Enum Value Rules

Enum elements represent literal JSON values.

For `str` enums:

- Bare identifiers are allowed and are interpreted as string literals.
  - `RUNNING` → `"RUNNING"`
- Quoted string literals are also allowed.
  - `"SECOND VOTE"`
- Bare identifiers inside enum blocks are treated as string values only.
  - They are NOT JSSN identifiers and do NOT participate in the global namespace.

Examples:

```jssn
type {
  Status = enum: str {
    RUNNING
    ENDED
    "ON HOLD"
  }
}
```

For non-string enums:

- Values MUST be valid JSON literals of the declared base type.

```jssn
type {
  RetryCount = enum: int {
    1
    2
    3
  }
}
```

Object and array enum values MUST use constant literal syntax (`!{}` / `![]`) to avoid ambiguity with type expressions.

```jssn
type {
  ConfigVariant = enum: obj {
    !{ a: 1 }
    !{ a: 2 }
  }
}
```

Restrictions:

- Enum elements MUST be literal values only.
- Enum elements MUST NOT include type expressions or constraints.
- If type-specific constraints per value are needed, authors MUST use union types with constant literals instead.

### 6.3.3 Inline Enum Forms

```jssn
str(enum A|B|C)
str(enum=["A","B","C"])
int(enum 1|2|3)
int(enum=[1,2,3])
(enum A|2)
(enum=["ANY", 2])
```

Type-less enums are allowed using `(enum ...)` as a standalone type expression.
Parentheses are REQUIRED to avoid ambiguity with other inline forms.

In this form, the element literals determine the allowed JSON values and tooling emits JSON Schema `enum` without an explicit `type` keyword.

In type-less enums, bare identifiers are interpreted as string literals (e.g., `ANY` → `"ANY"`).

### Notes

- Enums MAY contain any JSON literal values supported by JSON Schema `enum` (string, number/integer, boolean, null, object, array).
- The `enum A|B|C` form and the `enum=[...]` form are equivalent; the `A|B|C` form is syntactic sugar.
- These map directly to JSON Schema `enum`.
- Canonical enum normalization is defined in §8.2 and tooling MUST enforce it.
- Inline enum canonicalization preserves value order (no sorting); see §8.2.

Inline enum syntax and enum block syntax are equivalent in semantics. Both MUST emit JSON Schema `enum`.

Enum block syntax is recommended when enum values are numerous or long.

---

## 6.4 Constraints

Constraints restrict the value domain of a type.

### 6.4.1 Range Syntax (Recommended)

```jssn
int(1..7)
str(5..30)
arr(1..10)
obj(1..20)
```

### 6.4.2 Keyed Syntax (Also Allowed)

```jssn
int(min=1, max=7)
str(min=5, max=30)
```

### 6.4.3 Constraint Applicability

Range/size constraints are allowed only when the underlying base type is:

- `int`
- `str`
- `arr`
- `obj`

This rule is JSON Schema–compatible.

---

## 6.5 Format

### 6.5.1 Definition

A format is a **semantic refinement** of a base type.

- A format does NOT introduce a new data kind.
- Formats are most commonly applied to `str`.

### 6.5.x Design Intent: Format Handling

JSSN treats `format` as a semantic hint rather than a strict validation mechanism.

Design goals:

- Preserve JSON Schema `format` exactly as written.
- Allow arbitrary format identifiers.
- Avoid introducing validator-specific strictness.
- Keep JSSN compatible with a wide range of JSON Schema tooling.

JSSN does not define a strict-format mode and does not enforce format validation beyond JSON Schema semantics.

### 6.5.2 Syntax

```jssn
str(uuid)
str(email)
str(date-time)
str(email, 5..30)
```

### 6.5.2.1 Format Identifier Token Rules

- `<format>` is an **opaque identifier token**.
- Tooling MUST preserve the `<format>` string byte-for-byte when emitting JSON Schema.
- `<format>` MUST NOT contain whitespace, commas, parentheses, or the union operator `|`.
- `<format>` MAY contain ASCII letters, digits, `_`, `-`, and `.` (no normalization is performed).

### 6.5.3 Multiple Arguments

Within `str(...)`, at most one format identifier is allowed.

If more than one format identifier is specified, the schema is invalid.

Canonical argument order within `str(...)` MUST be:

1. The format identifier (if present)
2. The range constraint (if present)

Example canonical forms:

str(email)
str(email, 5..30)
str(5..30, email) // input allowed, canonicalized to str(email, 5..30)

---

## 6.6 Union Types

Union types are expressed using `|`.

```jssn
bool | null
uuid | null
int(0..7) | null
```

- `|` has the lowest precedence.
- Parentheses MAY be required for clarity.

---

## 6.7 Optional Fields

### Default Rule

All fields are required by default.

### Optional Marker

```jssn
history_id?: int
```

- `?` indicates the field MAY be omitted.
- This is distinct from allowing `null`.

---

## 6.8 Constant Literals

JSSN supports **constant literal values** to fix a field to an exact JSON value.
Constant literals are desugared to JSON Schema `const`.

### 6.8.1 Syntax

A constant literal is expressed by prefixing a value with `!`.

```jssn
enabled: !true
count: !3
mode: !"RUNNING"
nothing: !null
config: !{ a: 1, b: 2 }
pair: ![1, 2]
```

A constant literal MAY also be attached to a type expression using the standard **typed-const** form.

```jssn
count: int(!3)
id: str(uuid, !"550e8400-e29b-41d4-a716-446655440000")
retries: int(0..5, !1)
status: str(enum RUNNING|ENDED|INTERRUPTED, !"RUNNING")
```

Rules:

- Inside `T(...)`, a constant literal argument MUST be written as `!<literal>`.
- A constant literal argument, if present, MUST be the last argument.
- At most one constant literal argument is allowed.
- The argument list in `T(...)` is shared with existing constraints/format/enum arguments.

The legacy form `Type = !literal` is NOT part of JSSN v0.1 and is invalid.

### 6.8.2 Allowed Literals

The following literal kinds are supported:

- string
- integer
- number
- boolean
- null
- object
- array

### 6.8.3 Union Interaction

Constant literals MAY appear as members of union types.

```jssn
mode: !"AUTO" | !"MANUAL"
payload: !{ a: 1 } | null
```

These are desugared using JSON Schema `anyOf`.

Tooling MUST NOT rewrite literal unions into `enum`.

### 6.8.4 Semantics

- A constant literal restricts the value to be **exactly equal** to the given literal.
- A leading `!` has **no other semantic meaning**.
  - It does NOT imply override.
  - It does NOT imply precedence.
  - It does NOT affect optionality or requiredness.

---

## Annotation System

JSSN supports annotations for metadata and documentation.
Annotations do NOT affect validation semantics and are intended for humans and tooling only.

### Annotation Design Intent (Non-normative)

Annotations exist to support documentation, tooling, and schema evolution without affecting validation.

Design goals:

- Mirror JSON Schema annotation keywords where possible.
- Keep annotation syntax lightweight for human authors.
- Preserve annotation intent during canonicalization.
- Avoid introducing semantics beyond JSON Schema.

Annotations MUST NOT affect validation behavior.

### Annotation Placement

Annotations MAY appear in the following places:

- **Field-level**: after a field type / expression
- **Type-level**: after a **defined type** declaration (`Name = Expr`) inside `type { ... }` only
- **Schema-level**: on the `schema <Name>` declaration (either in the header or after the closing `}`)

Examples:

```jssn
type {
  UserId = str(uuid) @desc("User identifier") @example("550e8400-e29b-41d4-a716-446655440000")
}

schema Player @desc("Game participant") @example(!{ seat_no: 0 }) {
  seat_no: int(0..7) @desc("Seat number") @example(0) @example(1) @example(2)
  tags?: [str...] @example(!["mvp", "beta"])
}

schema CaseSnapshot {
  players: [Player...]
} @desc("Snapshot root")
```

Notes:

- If the same annotation key appears at multiple placements (e.g., type-level and field-level), JSSN v0.1 does not define merge/propagation semantics. Tooling MAY implement policies via `meta` (TBD).

### Annotation Shorthand Forms

JSSN provides shorthand forms for common annotations to improve readability.
These are syntactic sugar and do not introduce new semantics.

#### Example Shorthand

```jssn
@=value
```

Equivalent to:

```jssn
@example(value)
```

JSON Schema mapping:

```json
{ "examples": [value] }
```

##### Multiple Examples

Multiple examples MAY be specified by either repeating `@=` or by providing a comma-separated list in a single `@=`.

Both of the following are equivalent:

```jssn
example: int @=1 @=2 @=3
```

```jssn
example: int @=1,2,3
```

- Comma-separated lists are only allowed on a single line.
- Each list element MUST be a literal.
- Object and array examples MUST be written using constant literal forms: `!{ ... }` and `![ ... ]` to avoid ambiguity with type syntax.

---

#### Description Shorthand

```jssn
@:"text"
```

Equivalent to:

```jssn
@desc("text")
```

JSON Schema mapping:

```json
{ "description": "text" }
```

---

#### Default Shorthand

@~literal

Equivalent to:

@default(literal)

JSON Schema mapping:
{ "default": literal }

---

#### Standard Annotation Keywords (v0.1)

- `@=...` / `@example(...)` → JSON Schema `examples` (array)
- `@desc("...")` / `@description("...")` → JSON Schema `description` (string)
- `@~literal` / `@default(literal)` → JSON Schema `default`
- `@deprecated` → JSON Schema `deprecated: true`

---

#### Restrictions

- Shorthand forms are defined **only** for standard annotations listed above.
- Shorthand forms MUST NOT be used for user-defined annotations.
- Shorthand forms MUST NOT change validation semantics.
- Default values MUST be expressed using annotation syntax: `@~literal` (shorthand) or `@default(literal)` (canonical).
- Default annotations MAY appear on fields, defined types (`Name = Expr`), or schema declarations.

## 6.9 Default Values

Default values in JSSN are expressed as annotations and map directly to JSON Schema `default`.

Default values do NOT affect validation and are treated as metadata for tooling and documentation.

### 6.9.1 Syntax

Canonical form:

@default(literal)

Shorthand form:

@~literal

Examples:

retries: int @~3
name: str @~"guest"
enabled: bool @~true
config: obj @~!{ a: 1, b: 2 }

schema Example @~!{ retries: 3 } {
retries: int
}

type {
RetryCount = int(0..5) @~3
}

### 6.9.2 Semantics

- A default value does NOT affect validation.
- Default values MAY be used by tooling for UI initialization, code generation, and documentation.
- Default values MAY appear on required or optional fields.
- Default values do NOT imply optionality.

### 6.9.3 Compatibility

A default value MUST satisfy all declared constraints of its type.

retries: int(0..5) @~3 // valid
retries: int(0..5) @~10 // invalid

### 6.9.4 Interaction with Constant Literals

Defaults MAY coexist with constant literals:

retries: int(!1) @~1

The default MAY be redundant but SHOULD be preserved for documentation and future schema evolution.

### 6.9.5 Restrictions

- `@~` MUST prefix a literal.
- Object and array defaults MUST use constant literal forms:
  - `@~!{ ... }`
  - `@~![ ... ]`
- The legacy syntax `~literal` is invalid in JSSN v0.1.

---

## 6.10 Literal Types (Type Block)

Within the `type` block, a **defined type** declaration (`Name = ...`) or a **named inline type** declaration (`Name ^= ...`) MAY be assigned either (a) a literal JSON value, or (b) a typed-const type expression `T(..., !literal)`. These declare **literal types**.

```jssn
type {
  SingleValue = "a"
  Answer = 42
  Enabled = true
  LocalEnabled ^= true
  Nothing = null
  Pair = ![1, 2]
  Config = !{ a: 1, b: 2 }
  OneInt = int(!1)
  UuidConst = str(uuid, !"550e8400-e29b-41d4-a716-446655440000")
}
```

Semantics:

- A literal type fixes the value to be exactly equal to the given literal.
- Literal types are emitted as JSON Schema `const`.

Mapping intention (JSON Schema):

- `Name = <literal>` → `{ "const": <literal> }`
- `Name = T(..., !literal)` → `{ "type": <T>, ...constraints/format/enum..., "const": <literal> }`

Notes:

- String literals MUST be quoted.
- Object and array literal types MUST use the leading `!` (e.g., `![...]`, `!{...}`).
- Object and array literals MUST use `!{}` / `![]` to avoid ambiguity with type expressions.
- Literal types are distinct from enum constraints; enum blocks with a single element MUST canonicalize to a literal type.
- For typed literal aliases, the constant literal MUST be the final argument in `T(...)` (see §6.8.1).

### Literal Type Design Intent (Non-normative)

Literal types exist to distinguish between:

- a value constrained to a single literal (`const`)
- a broader type that may later expand

This allows schemas to evolve safely:
a literal type can later become a constrained type without changing field structure.

Literal types are therefore preserved explicitly rather than always normalized to enums or unions.

## 7. Additional Properties Policy

### 7.x Design Intent: Object Strictness

JSSN objects are closed by default to encourage explicit contracts.

This design:

- prevents accidental schema widening,
- improves validation predictability,
- and aligns with strongly-typed API design.

The spread (`...`) form exists as an explicit opt-in to open object behavior.

### 7.1 Default

All objects have:

```text
additionalProperties = forbid
```

by default.

This aligns with strict schema contracts.

### 7.2 Overrides (v0.1)

JSSN v0.1 supports overriding the default `additionalProperties = forbid` policy via the object spread form (`...`) inside an object type.

#### 7.2.1 No Spread (Default)

If an object contains no spread entry, it is closed:

- `additionalProperties: false`

#### 7.2.2 Spread Present (Override)

If an object contains a spread entry, it allows additional keys:

- `additionalProperties: schema(V)` for `{ ...: V }`
- `additionalProperties: {}` for `{ ...: any }`

The spread entry MAY be combined with fixed fields.

Example:

```jssn
{
  id: str
  tag?: str
  ...: str
}
```

Mapping intention:

- `properties: { id: schema(str), tag: schema(str) }`
- `required: ["id"]`
- `additionalProperties: schema(str)`

#### 7.2.3 Key Constraints with Spread

When a spread key constraint is present (length, format, or regex), tooling MUST emit `propertyNames` accordingly:

```jssn
{
  ...(1..20): V
}
```

```jssn
{
  ...(uuid): V
}
```

```jssn
{
  ...(/^(pattern)$/): V
}
```

Notes:

- JSON Schema applies `propertyNames` to all property names (including fixed keys). This is a JSON Schema behavior, not a JSSN-specific rule.
- JSON Schema `format` may be treated as a hint by some validators; see §6.5 and the warning in §6.2.

#### 7.2.4 JSON Schema Emission Summary (New)

This subsection summarizes how object entries map to JSON Schema.

Given an object type containing any combination of:

- `*` (global rule)
- `/regex/` entries (pattern rules)
- fixed fields
- spread entries (`...`)

Tooling MUST emit JSON Schema object keywords as follows:

- Fixed fields:
  - `properties` contains fixed field schemas
  - `required` contains all non-optional fixed field names

- Spread (`...`):
  - If present as `{ ...: V }`, emit `additionalProperties: schema(V)`
  - If present as `{ ...: any }`, emit `additionalProperties: {}`
  - If absent, emit `additionalProperties: false` (closed object)

- Pattern rules (`/regex/: V`):
  - Emit `patternProperties: { "<pattern>": schema(V) }` for each pattern rule.

- Global key constraints (`*(1..5): V`):
  - Emit `propertyNames: schema(str(1..5))`.

- Global value rule (`*: V*`):
  - The global value rule applies to ALL properties in the object, including fixed fields and pattern-matched properties.
  - When emitting field schemas and pattern schemas, tooling MUST compose `V*` with the local schema (AND).
  - Tooling SHOULD merge constraints to avoid emitting `allOf` when a lossless merge is possible.
  - If a lossless merge is not possible, tooling MAY emit `allOf: [schema(V*), schema(Vlocal)]`.

Notes:

- Spread entries (`...`) apply ONLY to additional (unknown) properties via `additionalProperties`.
- Fixed fields and pattern rules are NOT required to be compatible with a spread `{ ...: V }`.

---

### 7.3 Object Value Rule Composition (New)

This section defines how object-level value rules compose when multiple entry kinds are present.

#### 7.3.1 Base Value Rule

- If an object contains a `*` entry, its value schema `V*` is the **base value rule** for the object.
- Otherwise, the object has no base value rule.

Example:

```jssn
{
  *: int
  id: int
}
```

Valid.

```jssn
{
  *: int
  id: str
}
```

Invalid (the fixed field schema is incompatible with the global value rule).

#### 7.3.2 Fixed Fields

If a base value rule `Vbase` exists, then every fixed field schema `Vfield` MUST be compatible with it.

- If `Vfield` and `Vbase` have an empty intersection, the object schema is **invalid**.
- Tooling SHOULD merge constraints to emit a single schema for the field when possible.
- If a lossless merge is not possible, tooling MAY emit `allOf: [schema(Vbase), schema(Vfield)]`.

#### 7.3.3 Pattern Rules

If a base value rule `Vbase` exists, then every pattern rule schema `Vpat` MUST be compatible with it.

- If `Vpat` and `Vbase` have an empty intersection, the object schema is **invalid**.
- Tooling SHOULD merge constraints to emit a single schema for the pattern when possible.
- If a lossless merge is not possible, tooling MAY emit `allOf: [schema(Vbase), schema(Vpat)]`.

#### 7.3.4 Format Compatibility

For string schemas with `format`:

- If both sides specify a `format` and the formats differ, the intersection is empty and the schema is **invalid**.
- If both specify the same `format`, tooling MUST emit that same `format`.

## 8. Canonical Form & Normalization

### 8.x Design Intent: Canonical Form

Canonical form exists to support tooling and collaboration, not to restrict authoring.

Canonical output serves the following purposes:

- Stable diffs across formatting tools
- Deterministic emission from any compliant formatter
- Semantic identity comparison between schemas
- Predictable code generation and tooling behavior

Canonicalization SHOULD be applied by formatters and emitters, but authors are not required to write canonical syntax manually.

Canonicalization MUST NOT change semantics.  
If multiple syntactic forms are semantically identical, canonicalization MAY normalize them to a single stable form.

JSSN defines a canonical form to ensure **stable diffs**, **predictable tooling**, and **unambiguous semantics**.

### 8.0 Terminology: Lexicographic Order

When this document says **lexicographic order**, it means:

- Compare strings by **Unicode code point order** (not locale-aware).
- Comparison is performed left-to-right on code points.
- The first differing code point determines the ordering.
- If one string is a prefix of the other, the shorter string sorts first.

### 8.1 General Rules

- Canonical output MUST use canonical block order: `meta` → `type` → `schema`.
- Multi-line constructs MUST use **line breaks** as separators (see §2.3). Commas immediately before a line break are ignored.
- Canonical output SHOULD avoid trailing commas, even though they are tolerated by the parser.
- Whitespace is not semantically significant, but canonical output SHOULD follow the formatting conventions shown below.
- In canonical output, all constant literals MUST include the leading `!`, including scalar values.

- In canonical output, default annotations MUST be preserved, even when redundant due to `const`, to retain design intent.

- Within an object, canonical output MUST order entries as: `*` (if present), then `/regex/` entries, then fixed fields (required and optional), and finally a spread (`...`) entry (if present).
- In canonical output, a spread entry with value type `any` MUST be emitted as `...` (not `...: any`).

---

### 8.2 Enum Canonicalization

Allowed input forms include:

```jssn
str(enum A|B|C)
str(enum=["A","B","C"])
int(enum 1|2|3)
int(enum=[1,2,3])
(enum A|2)
(enum=["ANY", 2])
```

Canonical output rules:

- Canonical output MUST always emit the array form `enum=[...]` (never the bar-separated `enum A|B|C` form).
- Type-less enums MUST be emitted as `(enum=[...])` (without a base type). Parentheses MUST be preserved in canonical output.

- String enums MUST be emitted in array form as:
  ```jssn
  str(enum=["A", "B", "C"])
  ```
  (always using an array form and quoted values)
- Integer enums MUST be emitted in array form as:
  ```jssn
  int(enum=[1, 2, 3])
  ```
- Enum values MUST preserve declaration order; duplicates MUST be removed while preserving first-occurrence order (stable deduplication).
- In canonical output, all string values inside `enum=[...]` MUST be quoted string literals (even if written as bare identifiers in input).
- Single-value enums MUST be canonicalized to constant literals.
  - If a base type is present (e.g., `str(...)`, `int(...)`), canonical output MUST use the typed-const form:
    - `str(enum=["A"])` → `str(!"A")`
    - `int(enum=[3])` → `int(!3)`
  - If the enum is type-less, canonical output MUST emit an untyped constant literal:
    - `(enum=["A"])` → `!"A"`
- Type-block enum blocks are canonicalized separately: a single-value enum block MUST be emitted as a literal type alias (see §6.10).

---

### 8.3 Constraint Canonicalization

Constraints MAY be written using range syntax or keyed syntax.

Canonical output MUST use **range syntax**.

Examples:

- `int(min=1, max=7)` → `int(1..7)`
- `str(min=5, max=30)` → `str(5..30)`
- `int(min=1)` → `int(1..)`
- `arr(max=10)` → `arr(..10)`

For string types with both format and length constraints:

- Canonical argument order MUST be:
  ```jssn
  str(<format>, <range>)
  ```
  Example:
  ```jssn
  str(email, 5..30)
  ```

For object spread key constraints, canonical output MUST use the shorthand form:

```jssn
...(1..20): V
```

For objects that use header entries:

- `*` entry (if present) MUST appear first.
- `/regex/` entries MUST appear next, in lexicographic order by their regex literal (see §8.0).
- A spread entry MUST be last (if present).
- Ordering compares the raw `/.../` token text exactly as written (opaque), without any normalization.

For format-constrained spread keys, canonical output MUST use:

```jssn
...(uuid): V
```

(Using `...str(uuid): V` is not allowed in JSSN v0.1.)

---

### 8.4 Array and Tuple Canonicalization

#### Homogeneous Arrays

Canonical form:

```jssn
[T...]
```

Canonical multi-line form:

```jssn
[
  T...
]
```

#### Strict Tuples (Default)

Canonical single-line form:

```jssn
[T1, T2, T3]
```

Canonical multi-line form:

```jssn
[
  T1
  T2
  T3
]
```

Strict tuples have no additional elements beyond the listed positions.

#### Open Tuples (Any Tail)

Canonical shorthand:

```jssn
[T1, T2, ...]
```

Canonical output MUST NOT emit `any...` when `...` is sufficient.

#### Tail-Repeating Tuples

Canonical form:

```jssn
[T1, T2, T...]
```

If the tail type is a union, it MUST be parenthesized:

```jssn
[T1, T2, (A | B)...]
```

#### Array Length Constraints

- Canonical output MUST use the **prefix** form for length constraints:
  - `[X](1..3)` → `(1..3)[X]`
  - `[X](3)` → `(3)[X]`

---

### 8.5 Union Canonicalization

Unions are expressed using the `|` operator.

Canonical rules:

- Unions MUST be flattened:
  - `(A | B) | C` → `A | B | C`
- Unions MUST NOT be canonicalized into `enum` constraints, even when all union members are constant literals.
- Duplicate members MUST be removed.
- If a union contains `any`, the canonical result MUST be:
  ```jssn
  any
  ```
- If a union contains `null`, `null` MUST appear **last**.
- Non-null union members MUST be sorted in **lexicographic order** (see §8.0).
- Canonical formatting MUST use spaces around `|`.
- Constant literals MUST be preserved as union members and MUST retain the leading `!`.

Example:

Input:

```jssn
null | int | (str | int)
```

Canonical output:

```jssn
int | str | null
```

Note: A union of constant literals (e.g., `"ANY" | 2`) is emitted using JSON Schema `anyOf` + `const` members, while `enum("ANY"|2)` / `enum=["ANY", 2]` is emitted using JSON Schema `enum`. These are intentionally kept distinct in JSSN.

---

### 8.6 Schema Ordering

Schema blocks MUST be emitted in declaration order.

Canonicalization MUST NOT reorder schema blocks by name or by entry designation.
The `meta.entry` key, if present, identifies the entry schema without affecting ordering.

---

### 8.7 Annotation Canonicalization

Canonical output MUST emit **long-form** standard annotations for stability and simpler parsing.

Canonical rules:

- Shorthand inputs MUST be expanded:
  - `@=value` MUST be emitted as `@example(value)`
  - `@:"text"` MUST be emitted as `@note("text")`
- If `@=` is written using a comma-separated list, canonical output MUST emit repeated long-form examples:
  - `@=1,2,3` → `@example(1) @example(2) @example(3)`
- Multiple examples MUST be emitted as repeated `@example(<literal>)` annotations in the order they appear.
- Annotation order MUST be preserved as written.
- Annotation values MUST follow canonical literal formatting rules.
- For schema-level annotations, if an annotation is written after the closing `}`, canonical output MAY move it into the schema header (before `{`) without changing semantics.
- Object and array examples MUST be emitted using constant literal forms (`!{...}` / `![...]`).
- `@X` MAY be accepted as an input alias of `@deprecated`.
- Canonical output MUST emit `@deprecated` (never `@X`).

### 8.8 Named Type Reference Canonicalization

- References to **defined types** are written as bare `Name` and emit JSON Schema `$ref` to `#/$defs/Name`.
- References to **named inline types** are also written as bare `Name` and inline-expand at emission time.

Because usage syntax is identical, canonicalization MUST NOT rewrite references between defined vs inline types. The declaration form (`=` vs `^=`) is the single source of truth.

## 9. Invalid Schemas (Normative)

This section defines conditions under which a JSSN schema is **invalid**. Tooling MUST reject invalid schemas.

### 9.1 Type–Literal Mismatch

A schema is invalid if a literal value is not compatible with its declared type.

Examples:

```jssn
retries: int ~"three"
flag: bool(!"yes")
```

### 9.2 Invalid Constraint Applicability

A schema is invalid if a range/size constraint is applied to an unsupported base type.

Examples:

```jssn
bool(1..3)
null(1..)
```

### 9.3 Global Rule (`*`) Conflicts with Fixed Fields

When a global value rule is present, every fixed field schema MUST have a non-empty intersection with it. Otherwise the schema is invalid.

Example:

```jssn
{
  *: int
  id: str
}
```

### 9.4 Global Rule (`*`) Conflicts with Pattern Rules

A schema is invalid if a pattern rule schema has an empty intersection with the global value rule.

Example:

```jssn
{
  *: int
  /^i-/: str
}
```

### 9.5 Format Conflicts

For string schemas with `format`, if a global rule and a local rule both specify a `format` and the formats differ, the schema is invalid.

Example:

```jssn
{
  *: str(uuid)
  id: str(email)
}
```

### 9.6 Enum and Constant Conflicts

A schema is invalid if an `enum` constraint and a `const` literal are mutually exclusive.

Examples:

```jssn
status: str(enum A|B, !"C")
count: int(enum 1|2, !3)
```

### 9.7 Default Value Violations

A schema is invalid if a default value (`@~literal` or `@default(literal)`) does not satisfy the declared type, constraints, or format.

Example:

```jssn
retries: int(0..5) @~10
```

### 9.8 Object Entry Multiplicity Errors

An object schema is invalid if it declares:

- more than one global rule entry (`*`), or
- more than one spread entry (`...`).

Examples:

```jssn
{
  *: int
  *: num
}

{
  ...: int
  ...: str
}
```

### 9.9 Global Name Conflicts

A document is invalid if any two declarations resolve to the same identifier in the global namespace.

This includes conflicts between:

- a defined type `Name = ...` and a named inline type `Name ^= ...`
- any `schema Name` and any `Name = ...` or `Name ^= ...` in `type {}`

Examples (invalid):

```jssn
type {
  SeatNo = int(0..7)
  SeatNo ^= int(0..7)
}
```

```jssn
type {
  SeatNo = int(0..7)
}

schema SeatNo {
  id: int
}
```

### 9.10 Name Conflicts Between `type` and `schema`

A document is invalid if any `schema <Name>` conflicts with a name declared in `type {}` (either a defined type or a named inline type).

Example:

```jssn
type {
  SeatNo = int(0..7)
}

schema SeatNo {
  id: int
}
```

### 9.11 Multiple Format Identifiers

A schema is invalid if more than one format identifier is specified within `str(...)`.

Example (invalid):

```jssn
id: str(uuid, email)
```

## 10. Versioning

### 10.1 JSSN Version

Declared via:

```jssn
meta {
  jssn_version: "0.1"
}
```

The `jssn_version` key is required (see §3.4).

### 10.2 Compatibility Policy

Backward compatibility and deprecation rules are TBD.

---

## 11. Future Work (Non-normative)

The following topics are intentionally out of scope for v0.1.

They are reserved for future versions and may evolve independently of the core language.

- Import / module system
- Multi-file bundling strategy
- External schema referencing conventions
