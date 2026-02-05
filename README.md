# JSSN (JSON Schema Symbolized Notation)

**JSSN** is a schema‑first DSL designed to generate canonical JSON Schema in a way that is readable, expressive, and deterministic.

It focuses on **human‑authored schema design**, while using JSON Schema as a compilation target.

> Status: experimental language design (v0.1 draft)

---

## Why JSSN?

Writing raw JSON Schema directly is often:

- verbose
- repetitive
- hard to diff
- difficult to reason about structurally

JSSN exists to provide:

- a concise schema authoring language
- strong canonicalization rules
- deterministic JSON Schema emission
- reusable type definitions
- readable constraints and metadata

JSSN is not a replacement for JSON Schema —  
it is a **language that compiles into JSON Schema**.

---

## Design Goals

JSSN is designed with the following goals:

### Human‑first authoring

Readable, writable, and structurally clear schema definitions.

### Canonical output

Two semantically identical schemas should emit identical JSON Schema.

### Deterministic compilation

No ambiguity in how a JSSN document maps to JSON Schema.

### Separation of concerns

Clear distinction between:

- type
- constraint
- format
- metadata (annotations)

### JSON Schema compatibility

Everything expressible in meaningful JSON Schema should be representable in JSSN.

---

## Example

```jssn
meta {
  jssn_version: "0.1"
  entry: CaseSnapshot
}

type {
  SeatNo = int(0..7)
  uuid ^= str(uuid)
}

schema Player {
  id: uuid
  seat: SeatNo
}

schema CaseSnapshot {
  case_id: uuid
  players: [Player...]
}
```

This compiles into canonical JSON Schema with:

- `$defs` for reusable types
- `$ref` usage
- deterministic structure
- consistent constraints

---

## Core Concepts

### Schema‑first DSL

JSSN documents describe schema structures first, not runtime data.

### JSON Schema as target

JSSN is compiled/emitted into JSON Schema.  
JSON Schema remains the validation authority.

### Canonical form

JSSN defines canonical output rules so that:

- formatting is stable
- diffs are meaningful
- emitters can normalize structure

### Type system

JSSN supports:

- primitive types
- constraints and ranges
- enums
- const literals
- reusable types
- inline vs `$defs` types
- arrays and tuples
- object property rules

### Annotation system

Metadata is supported without affecting validation:

- description
- examples
- default
- deprecated

Annotations map directly to JSON Schema annotations.

---

## Project Status

This repository currently contains:

- JSSN language draft (v0.1)
- design exploration
- internal documentation
- personal experimentation

It is **not yet a production‑ready language** and has no official tooling.

---

## Repository Structure

```
/spec
  JSSN-Spec.md           # canonical English spec (SSOT)
  spec.ko.summary.md     # personal Korean summary
```

Additional tooling or parser implementations may be added later.

---

## Intended Use

JSSN is currently designed for:

- personal schema design exploration
- JSON Schema authoring experiments
- language design experimentation

Future possibilities include:

- parser/emitter implementation
- formatter
- schema tooling
- public language release

---

## License

TBD
