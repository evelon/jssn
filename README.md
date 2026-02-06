# JSSN (JSON Schema Simplified Notation)

JSSN is a human-oriented authoring language for JSON Schema.

It is designed for developers who have used JSON Schema before, but find it
difficult to read, write, review, and maintain as schemas grow in size and depth.
JSSN focuses on clarity, intent, and predictable structure, while remaining
directly translatable to standard JSON Schema.

Links:

- Spec: `JSSN-Spec.md`
- Examples: `examples/`

---

## Why JSSN

JSON Schema is a powerful and widely adopted specification, but it is primarily
designed as a machine-oriented interchange format rather than a language for
humans to author directly.

In practice, authoring JSON Schema often becomes problematic:

- Deep nesting quickly harms readability
- Small structural mistakes are easy to introduce and hard to detect
- Meaningful diffs become difficult as schemas grow verbose
- Expressing intent often requires indirect or repetitive constructs

JSSN exists to address these issues.

JSSN is not a replacement for JSON Schema. Instead, it is an authoring notation
that allows developers to describe schemas in a concise, readable form, and then
emit standard JSON Schema from it.

The language intentionally targets a well-defined subset of JSON Schema features,
favoring predictability, portability, and ease of reasoning over maximal
expressiveness.

---

## Quick Look

A minimal example showing what JSSN looks like:

```jssn
{
  id: str(uuid)
  status: str(enum ACTIVE|INACTIVE)
  score: int(0..100)
}
```

This example illustrates the core ideas of JSSN:

- JSON-like structure
- Explicit types
- Constraints expressed inline
- Compact enum notation

---

## What JSSN Is

JSSN is an authoring language that produces JSON Schema.

It provides:

- A compact syntax for common schema patterns
- Inline constraints that make intent explicit
- Readable structures that scale better than raw JSON Schema

JSSN does not attempt to expose every feature of JSON Schema. Constructs that do
not map cleanly or predictably to standard JSON Schema are intentionally excluded.

---

## Design Scope

JSSN is designed around the following principles:

- **Human readability first**  
  Schemas should be easy to scan, review, and discuss.

- **Direct JSON Schema mapping**  
  Every JSSN construct maps directly to standard JSON Schema without relying on
  implementation-specific behavior.

- **Subset by design**  
  JSSN intentionally avoids features that introduce ambiguity, excessive
  complexity, or validator-dependent semantics.

JSSN favors being easy to reason about over being maximally expressive.

---

## Format Support

JSSN allows arbitrary `format` values supported by JSON Schema.
Format validation behavior depends on the target validator and is not enforced
by JSSN itself.

---

## Status

**Experimental**

The language and specification are still evolving. Syntax and semantics may
change based on feedback and real-world usage.

---

## Documentation

- Language specification: `JSSN-Spec.md`
- Example schemas: `examples/`
