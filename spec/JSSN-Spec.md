# JSSN (JSON Schema Symbolized Notation)

## JSSN Specification — Draft v0.2

> v0.2 defines the core JSSN language only.  
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
- JSSN separates concerns such as data kind, constraint, format, and metadata explicitly.
- Every construct in JSSN MUST be either:
  - directly representable in JSON Schema, or
  - reducible to a JSON Schema–representable construct via desugaring.

In this specification, the term **type** refers to any **type expression** that may appear on the right-hand side of a field declaration.  
A type describes the shape and constraints of values, independent of how that type is produced or named.

Some constructs in JSSN introduce **named types**.  
Such constructs are referred to as **type producers** and are defined formally in §6.0.

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
- `inline { ... }` — optional, at most one
- `def <Name> <TypeExpr>` — required, one or more
  - `<TypeExpr>` may be **any valid type expression**, including object, array, scalar, union, enum, or literal.
  - If `<TypeExpr>` is an **object type**, it is written using `{ ... }` (block form).
  - If `<TypeExpr>` is an **array type**, it is written using `[ ... ]` (array or tuple form).
  - Otherwise, `<TypeExpr>` is written inline on the same line as the `def` header.
  - `<TypeExpr>` MUST be a single, complete type expression and MUST NOT contain additional declarations.

Example:

Example:

```jssn
meta {
  jssn_version: "0.2"
}

def Root {
  id: int
}

def IdList [int...]

def Enabled !true
```

### 2.2 Canonical Block Order

When normalized, blocks MUST appear in this order:

1. `meta` (one)
2. `inline`
3. `def` (one or more)

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

> A JSSN document therefore separates _structural reuse_ (`def`) from _structural composition_ (`inline`) explicitly at the block level.

## 3. Meta Block

### 3.1 Purpose

The `meta` block contains **document-level metadata**.

- It does not define data structure.
- It does not affect schema semantics.
- It is intended for humans and tooling.
  The `entry` key identifies which `def` acts as the **document root**.  
  This designation is used by tooling to select the **entry schema** when emitting JSON Schema.

### 3.2 Syntax

```jssn
meta {
  jssn_version: "0.2"
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
- If a document contains more than one `def` block, `entry` MUST be present and MUST equal the name of one declared `def`.
- If a document contains exactly one `def` block and `entry` is absent, tooling MUST treat that schema as the entry schema.

> **Entry semantics note:**  
> JSSN defines the entry at the _authoring language level_ via `meta.entry`.  
> When emitting JSON Schema, this same entry is represented as the **entry schema**, typically via a top-level `$ref` to the corresponding definition under `$defs`.  
> These are two representations of the same conceptual root at different layers and are intentionally kept in sync.

---

## 4. Inline Block

### 4.1 Purpose

The `inline` block defines **inline type aliases**.
These aliases are **type producers** whose names are always expanded inline at their usage sites.
Inline alias declarations never emit `$defs` entries on their own, and every usage of an inline alias name is inline-expanded at the usage site.

All user-declared identifiers in a JSSN document share a single global namespace:

- inline alias names (`Name = ...`)
- def names (`def Name { ... }`)

These base identifiers MUST be globally unique. If two declarations resolve to the same identifier string, the document is invalid.

---

### 4.2 Type Alias (Inline Only)

```jssn
inline {
  SeatNo = int(0..7)
  Status = str(enum RUNNING|ENDED)
}
```

Rules:

- `Name = Expr` declares an inline alias.
- Inline aliases MUST NOT generate `$defs` entries.
- Every usage of `Name` MUST inline-expand `Expr`.
- Tooling MUST NOT emit `$ref` for inline aliases.

### 4.3 Usage Rules

All type names declared in `inline {}` are inline-expanded at usage sites.  
`$ref` is never emitted for inline aliases.

### 4.4 Format Alias

A format alias is an inline alias and is always inline-expanded.

### 4.5 Inline-level Annotation Rules

- Annotations MAY appear on inline alias declarations inside `inline { ... }`.
- Inline alias annotations are **copied to every expansion site**.
- If an inline alias is used at a site that already has the same annotation key (e.g., both provide `@description(...)`), the **use-site (field-level) annotation takes precedence** and the copied annotation MUST NOT be emitted for that key at that site.
- `@example(...)` is special: multiple examples MAY be combined by appending the alias examples after the use-site examples while preserving relative order. (No deduplication is required.)
- This copy/precedence rule affects **annotation emission only** and MUST NOT affect validation semantics.

## 5. Def Block

Each `def <Name> <TypeExpr>` defines a reusable named type in JSSN.  
When emitted to JSON Schema, each `def` is represented as a named entry under `$defs`.

> A `def` block is a **type producer**.  
> It introduces a named type that may be referenced by name in other type expressions.
>
> The `<TypeExpr>` of a `def` may be **any valid type expression**.
> If `<TypeExpr>` is an **object type**, it is written using `{ ... }` (block form).
> If `<TypeExpr>` is an **array or tuple type**, it is written using `[ ... ]` (block form).
> All other types (scalar, union, enum, literal) are written inline on the same line as the `def` header.

The document entry is selected via `meta.entry` (or by the implicit single-definition rule) and determines which definition becomes the **entry schema** in the emitted JSON Schema.

### 5.1 Purpose

A `def` block defines exactly one **named type definition**, which may be any valid type expression (object, array, scalar, union, enum, or literal).

```jssn
def CaseSnapshot {
  ...
}

def IdList [int...]

def Enabled !true
```

Additional examples:

```jssn
def Flags [bool...]

def Mode "AUTO" | "MANUAL"

def Count int(0..10)
```

### 5.2 Rules

- Named identifiers MUST be globally unique within the document (see §4.1): schema names and type alias names (`Name = ...`) share a single namespace.
- Def blocks define a named type, which may be any valid type expression.
- If the type is an object, it is written in block form `{ ... }` or as a field list (object shorthand).
- Non-object types MUST be written as a single inline type expression following the `def <Name>` header.
- Type producer declarations are NOT allowed inside def blocks.

### 5.3 Def References (New)

Defs MAY be referenced by name from within other defs.

Example:

```jssn
def Player {
  seat_no: int(0..7)
}

def CaseSnapshot {
  players: [Player...]
}
```

Mapping intention:

- Each `def <Name> <TypeExpr>` is emitted as a named schema definition (e.g., under JSON Schema `$defs`).
- References to `<Name>` are emitted as `$ref` to that definition.

Because `def` blocks are type producers, references to `<Name>` always refer to the produced type, never to the declaration itself.

Notes:

- Recursive and mutually recursive def references are allowed and map to JSON Schema `$ref`.
- The document MAY designate a single entry schema via `meta.entry`.
- If a document contains more than one `def` block, `meta.entry` is REQUIRED (see §3.4).

> The JSSN document entry and the JSON Schema entry schema are conceptually identical; the difference lies only in representation (JSSN metadata vs emitted `$ref`).

Emission note (normative): Tooling MUST emit all `def <Name> <TypeExpr>` blocks as named definitions under JSON Schema `$defs`. The entry schema (determined by §3.4) MUST be emitted as a top-level `$ref` to `#/$defs/<EntryName>`.

> Only `def <Name>` declarations produce `$defs` entries.  
> Inline aliases never do.

---

## 6. Type System

### 6.0 Terminology: Types and Type Producers

A **type** is any type expression that may appear on the right-hand side of a field declaration.

Examples of types include:

- primitive types (`int`, `str`, `bool`, ...)
- composite types (objects, arrays, tuples, unions)
- references to named types produced by `inline` aliases or `def` blocks

A **type producer** is a declaration construct that introduces a **named type** which may later be referenced by name.

In JSSN v0.1, the following constructs are type producers:

- inline alias declarations (`Name = Expr` inside `inline {}`)
- def declarations (`def <Name> <TypeExpr>`)

Type producers do not appear directly in field positions; their produced names do.

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

#### Homogeneous Arrays (Prefix-Only)

Homogeneous arrays are written using the **prefix array operator**: `[]`.

- The array type is formed as `[]T`, where the brackets `[]` immediately precede a single type expression `T`.
- The `[]` operator binds only to the immediately following single type expression.
- The postfix form `T[]` and postfix length forms are **invalid** in JSSN and MUST NOT be used.

**Array Length Constraints:**

- To constrain length, attach immediately after `[]`:
  - `[](min..max)T` — array length constrained to min..max (inclusive).
  - `[](n)T` — array length exactly `n`.
  - Keyed length constraints are also allowed:
    - `[](min=..., max=...)T`
    - `[](min=...)T`
    - `[](max=...)T`
  - Canonicalization for keyed → range:
    - `min=1,max=2` → `(1..2)`
    - `min=1` → `(1..)`
    - `max=2` → `(..2)`
    - `min=max=n` → `(n)`

- The length constraint attaches directly after `[]` and before the element type.
- The `[]` operator and its length constraint always apply only to the immediately following type expression.

**Union Rule for Arrays:**

- If the element type is a union, **parentheses are REQUIRED** around the union type.
  - Valid: `[](int | str)`
  - Invalid: `[]int | str` (this would be parsed as an array of `int`, unioned with `str`)
- The union operator `|` has lower precedence than the array operator `[]`.

Semantics:

- All items MUST satisfy `T`.
- If a length constraint is present, array length MUST be within the specified bounds.

Mapping intention (JSON Schema):

- `items: schema(T)`
- Length constraints map to `minItems`/`maxItems`:
  - `minItems = min`
  - `maxItems = max`

**Examples:**

```jssn
[]int
[]str(5..30)
[](uuid | null)
[](int | str)
[](str(enum=["A", "B"]))
[](2..4)int
[](min=1, max=3)str
[](3)(int | str)
```

Multiline example:

```jssn
[]{
  id: int
  name: str
}
```

**Nested array with length:**

```jssn
[](3)[](2..4)T
```

with strings,

```jssn
[](3)[](2..4)str(4..6)
```

##### Rationale (Non-normative)

JSSN places array length constraints **immediately after the `[]` prefix** (as in `[](2..4)T`) and forbids postfix array or length forms. This avoids ambiguity and excessive parentheses when working with complex element types or nested arrays.

If JSSN allowed postfix length constraints (e.g. `[]T(2..4)`), then nested or parenthesized types would require excessive parentheses to clarify binding. For example, to express an array of strings of length 2..4, length-constrained, you would have to write something like:

```jssn
([](str(4..6)))(2..4)
```

Prefixing length after `[]` keeps the operator and its modifiers together, and improves readability for nested arrays:

- Postfix: `[][]T(2..4)(3)`
- Prefix: `[](3)[](2..4)T`

Therefore, only the prefix form `[]`, with length constraints directly after `[]`, is allowed. Postfix `T[]` and postfix length forms are invalid.

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

- `[T1, ...]` is also allowed (a tuple with a single required prefix and an open tail).

Semantics:

- The array MUST have at least as many items as the fixed prefix.
- The first items MUST satisfy the fixed types.
- Additional items MAY be any JSON value.

Mapping intention (JSON Schema 2020-12):

- `prefixItems: [schema(T1), schema(T2)]`
- `items: {}`
- `minItems = prefixLen`

##### Tail-Typed Open Tuples

Tuples MAY specify a typed tail, requiring all additional items to match a type.

```jssn
[T1, T2, ...T]
```

Semantics:

- The array MUST have at least as many items as the fixed prefix.
- The first items MUST satisfy each `Ti`.
- Additional items MUST satisfy `T`.

Mapping intention (JSON Schema 2020-12):

- `prefixItems: [schema(T1), schema(T2)]`
- `items: schema(T)`
- `minItems = prefixLen`

If the tail type is a union, it MUST be parenthesized and written as `...(A | B)` (no whitespace):

- `[T1, T2, ...(A | B)]` means the tail items must be of type `A | B`.
- If `T` is a union, it MUST be parenthesized and written as `...(A | B)` (no whitespace).

Restrictions:

- Typed tail requires at least one fixed prefix item; `[...T]` is invalid. Use `[]T` for homogeneous arrays.
- Only one tail marker (`...` or `...T`) is allowed per tuple; both forms cannot appear together.

##### Tuple Tail Length Constraints

Tuple tail length constraints attach to the tail marker, not to the whole tuple.

- **Any-tail open tuple tail count:**
  - `[T1, T2, ...(2..5)]` means the tail has 2..5 items of `any` type.
  - Mapping: `minItems = prefixLen + 2`, `maxItems = prefixLen + 5`, `items: {}`
- **Typed tail count:**
  - `[T1, T2, ...(2..4)T]` means the tail has 2..4 items of type `T`.
  - `[T1, T2, ...(3)T]` means the tail has exactly 3 items of type `T`.
  - Whitespace is discouraged between the tail count and the tail type.
  - Mapping: `items: schema(T)`, `minItems = prefixLen + min`, `maxItems = prefixLen + max`
- **Typed tail with union:**
  - For a union tail with no count, write `[T1, T2, ...(A | B)]`.
  - For a union tail with a count, write `[T1, T2, ...(2..4)(A | B)]`.
  - If `T` is a union, it MUST be parenthesized and written as `...(A | B)` (no whitespace).
- **Invalid cases:**
  - Tail count with strict tuple (no tail marker) is invalid (e.g., `[T1, T2](2..5)` is invalid).
  - Only one tail marker per tuple; `...` and `...T` cannot both appear.
  - Typed tail with zero prefix is invalid; `[...T]` and `[(...)(A|B)]` with zero prefix are not allowed; use `[]T`.

##### Note: `[T, ...]` vs `[]T`

- `[]T`, `[](n)T`, `[](min..max)T` are homogeneous arrays.
- `[T, ...]` is an open tuple with a required first item `T` and an `any` tail.
- `[T, ...T]` is an open tuple with a required first item `T` and a typed tail.

---

## 6.3 Enum

### 6.3.1 Enum Block Syntax (Inline Block Only)

Enums MAY be declared as reusable types inside the `inline` block using a block form.

```jssn
inline {
  VoteKind = enum: str {
    FIRST_VOTE
    "SECOND VOTE"
    "INTERRUPTED"
  }
}
```

Rules:

- Enum block syntax is allowed ONLY inside the `inline` block.
- Enum blocks MUST NOT appear inline inside `def` fields.
- The declared enum becomes a named type alias and may be referenced like any other type.
- The base type (`str`, `int`, etc.) determines the JSON Schema type.
- Enum elements represent literal JSON values and are emitted as JSON Schema `enum`.
- Inline enum syntax (e.g., `str(enum ...)`) MUST NOT be used inside `inline { ... }`. Use enum blocks instead.
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
inline {
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
inline {
  RetryCount = enum: int {
    1
    2
    3
  }
}
```

Object and array enum values MUST use constant literal syntax (`!{}` / `![]`) to avoid ambiguity with type expressions.

```jssn
inline {
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

In this form, the element literals determine the allowed JSON values and tooling emits JSON Schema `enum` without an explicit `inline` keyword.

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
- **Inline-alias level**: after an inline alias declaration (`Name = Expr`) inside `inline { ... }`
- **Def-level**: on the `def <Name>` declaration (either in the header or after the closing `}`)

Examples:

```jssn
inline {
  UserId = str(uuid) @description("User identifier") @example("550e8400-e29b-41d4-a716-446655440000")
}

def Player @description("Game participant") @example(!{ seat_no: 0 }) {
  seat_no: int(0..7) @description("Seat number") @example(0) @example(1) @example(2)
  tags?: [str...] @example(!["mvp", "beta"])
}

def CaseSnapshot {
  players: [Player...]
} @description("Snapshot root")
```

Notes:

- If the same annotation key appears at multiple placements (e.g., inline-alias and field-level),
  field-level annotations take precedence for emission. See §4.5 for rules.
- For `def` blocks whose type expression is written in **block form** (`{ ... }` for objects,
  `[ ... ]` for arrays or tuples), def-level annotations MAY appear either:
  - in the `def <Name>` header, or
  - after the closing block.
- For `def` blocks whose type expression is written **inline** (scalar, union, enum, or literal),
  def-level annotations MAY appear **only in the header**.

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
- `@description("...")` → JSON Schema `description` (string)
- `@default(literal)` → JSON Schema `default`
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

inline {
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

---

## 6.10 Literal Types (Inline Block)

Within the `inline` block, a type alias declaration (`Name = ...`) MAY declare a **literal type** using the constant-literal prefix `!`, or a **typed constant** using `T(..., !literal)`. Literal types emit JSON Schema `const`.

```jssn
inline {
  SingleValue = !"a"
  Answer = !42
  Enabled = !true
  Nothing = !null
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

- `Name = !<literal>` → `{ "const": <literal> }`
- `Name = T(..., !literal)` → `{ "type": <T>, ...constraints/format/enum..., "const": <literal> }`

Notes:

- String literal constants MUST be written as `!"..."` (quoted string literal prefixed with `!`).
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

Canonical form exists to support tooling, collaboration, and long-term maintenance.

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

- Canonical output MUST use canonical block order: `meta` → `inline` → `def`.
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

This section defines the canonical surface forms for array and tuple type expressions.
Canonicalization MUST follow the syntax and precedence rules defined in §6.2.

#### Homogeneous Arrays

Canonical form uses the **prefix array operator** `[]`.

```jssn
[]T
```

If a length constraint is present, it MUST appear immediately after `[]`:

```jssn
[](2..4)T
[](3)T
```

Canonical multi-line form (for complex element types):

```jssn
[]{
  field: int
}
```

Rules:

- Canonical output MUST NOT use postfix array forms (`T[]`).
- Canonical output MUST NOT use postfix length constraints.
- The `[]` operator always binds to exactly one following type expression.
- If the element type is a union, it MUST be parenthesized:

```jssn
[](A | B)
```

#### Strict Tuples (Default)

Strict tuples list a fixed number of positional item types.

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

Strict tuples:

- Have no tail marker.
- Implicitly disallow additional items.
- MUST NOT carry length constraints.

#### Open Tuples (Any Tail)

Open tuples allow additional items of unrestricted type.

Canonical form:

```jssn
[T1, T2, ...]
```

Rules:

- `...` indicates an open tail of type `any`.
- Canonical output MUST NOT emit `any...`.
- The tuple length is at least the prefix length.

#### Typed Tail Tuples

Tuples MAY specify a typed tail using `...T`.

Canonical form:

```jssn
[T1, T2, ...T]
```

If the tail type is a union, it MUST be parenthesized:

```jssn
[T1, T2, ...(A | B)]
```

Rules:

- Typed tails require at least one fixed prefix item.
- `[...T]` is invalid; use `[]T` for homogeneous arrays.
- Only one tail marker (`...` or `...T`) is allowed.

#### Tuple Tail Length Constraints

Tuple length constraints apply **only to the tail**, never to the entire tuple.

Any-tail open tuple:

```jssn
[T1, T2, ...(2..5)]
```

Typed tail with count:

```jssn
[T1, T2, ...(2..4)T]
[T1, T2, ...(3)T]
```

Union tail with count:

```jssn
[T1, T2, ...(2..4)(A | B)]
```

Rules:

- Tail length constraints MUST attach directly to `...`.
- Whitespace between the count and the tail type is discouraged.
- Strict tuples (without `...`) MUST NOT have length constraints.
- Canonical output MUST NOT rewrite tuple forms into array forms or vice versa.

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

Def blocks MUST be emitted in declaration order.

Canonicalization MUST NOT reorder def blocks by name or by entry designation.
The `meta.entry` key, if present, identifies the entry schema without affecting ordering.

---

### 8.7 Annotation Canonicalization

Canonical output MUST emit **long-form** standard annotations for stability and simpler parsing.

Canonical rules:

- Shorthand inputs MUST be expanded:
  - `@=value` MUST be emitted as `@example(value)`
  - `@:"text"` MUST be emitted as `@description("text")`
  - ``@~literal MUST be emitted as `@default(literal)``
- If `@=` is written using a comma-separated list, canonical output MUST emit repeated long-form examples:
  - `@=1,2,3` → `@example(1) @example(2) @example(3)`
- Multiple examples MUST be emitted as repeated `@example(<literal>)` annotations in the order they appear.
- Annotation order MUST be preserved as written.
- Annotation values MUST follow canonical literal formatting rules.
- For def-level annotations, if an annotation is written after the closing `}`, canonical output MAY move it into the def header (before `{`) without changing semantics.
- Object and array examples MUST be emitted using constant literal forms (`!{...}` / `![...]`).
- `@X` MAY be accepted as an input alias of `@deprecated`.
- Canonical output MUST emit `@deprecated` (never `@X`).

### 8.8 Def Block Canonicalization

Def blocks define named reusable types and have a canonical structural form.

Canonical rules:

- A `def` block MUST be emitted using the form:

  def <Name> <TypeExpr>

  where `<TypeExpr>` is a single type expression.

- If the defined type is an object, the canonical form MUST use an object literal:

  def <Name> {
  ...
  }

- If the defined type is an array, scalar, union, enum, or literal, the canonical form MUST place the type expression on the same line as the `def` header.

  Examples (canonical):

  def Flags [bool...]
  def Enabled bool
  def Disabled !false
  def Status (enum=["RUNNING", "ENDED"])
  def Count int(0..5)
  def FixedCount int(!3)

- Canonical output SHOULD place the type expression immediately after `<Name>` without introducing an extra block level.

- A `def` block MUST NOT omit the leading `!` for constant literals.
  For example:

  def Invalid false

  is invalid and MUST NOT appear in canonical output.

- Canonicalization MUST NOT rewrite a `def` into an inline alias or vice versa.
  Whether a named type is inline-expanded or emitted via `$defs` is determined solely by the declaration kind, not by usage.

### 8.9 Named Type Reference Canonicalization

- References to **inline aliases** are written as bare `Name` and are always inline-expanded at emission time.
- References to **defs** are written as bare `Name` and are emitted as `$ref` to `#/$defs/Name`.

Because usage syntax is identical, canonicalization MUST NOT rewrite references. The declaration form (inline vs def) is the single source of truth for whether emission expands inline or emits `$ref`.

## 9. Invalid Schemas (Normative)

This section defines conditions under which a JSSN schema is **invalid**. Tooling MUST reject invalid schemas.

### 9.1 Type–Literal Mismatch

A schema is invalid if a literal value is not compatible with its declared type.

Examples:

```jssn
retries: int @~"three"
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

- any `def Name` and any `Name = ...` in `inline {}`

Examples (invalid):

```jssn
inline {
  SeatNo = int(0..7)
}

def SeatNo {
  id: int
}
```

### 9.10 Name Conflicts Between `inline` and `def`

A document is invalid if any `def <Name>` conflicts with a name declared in `inline {}`.

Example:

```jssn
inline {
  SeatNo = int(0..7)
}

def SeatNo {
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
  jssn_version: "0.2"
}
```

The `jssn_version` key is required (see §3.4).

### 10.2 Compatibility Policy

Backward compatibility and deprecation rules are TBD.

### 10.3 Changes in v0.2 (Non-normative)

- Renamed top-level blocks (`type` → `inline`, `schema` → `def`)
- Generalized `def` blocks to allow any type expression (object, array, scalar, union, enum, literal)
- Introduced a prefix-only array operator `[]` and forbade postfix array forms
- Defined array length constraints as prefix modifiers attached directly after `[]`
- Clearly distinguished homogeneous arrays from tuple-shaped arrays
- Refined tuple syntax, including:
  - strict tuples with fixed length
  - open tuples with `...` (any tail)
  - typed tail tuples using `...T`
  - tail-only length constraints using `...(n)` and `...(min..max)`
- Explicitly disallowed rewriting between array and tuple forms during canonicalization
- Clarified annotation placement and precedence rules
- Strengthened canonicalization rules for emission stability

---

## 11. Future Work (Non-normative)

The following topics are intentionally out of scope for v0.1.

They are reserved for future versions and may evolve independently of the core language.

- Import / module system
- Multi-file bundling strategy
- External schema referencing conventions
