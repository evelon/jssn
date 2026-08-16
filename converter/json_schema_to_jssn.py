#!/usr/bin/env python3
"""Convert a JSON Schema file into JSSN, per spec/types.md.

Only constructs defined in spec/types.md are supported: the `type` keyword
(string/number/integer/boolean/object/array/null), `properties` for objects,
and `items`/`prefixItems` for arrays. Anything not yet part of the JSSN spec
($ref, allOf/anyOf/oneOf, enum, const, required, format, additionalProperties,
etc.) is silently dropped from the output.
"""

import argparse
import json
import sys

INDENT = "  "

TYPE_ALIASES = {
    "string": "str",
    "number": "num",
    "integer": "int",
    "boolean": "bool",
    "object": "obj",
    "array": "arr",
    "null": "null",
}


def convert(schema, level=0):
    if not isinstance(schema, dict):
        return None

    node_type = schema.get("type")
    if isinstance(node_type, list):
        supported = [t for t in node_type if t in TYPE_ALIASES]
        node_type = supported[0] if supported else None

    if node_type is None:
        if isinstance(schema.get("properties"), dict):
            node_type = "object"
        elif "items" in schema or "prefixItems" in schema:
            node_type = "array"

    if node_type == "object":
        return convert_object(schema, level)
    if node_type == "array":
        return convert_array(schema, level)
    return TYPE_ALIASES.get(node_type)


def convert_object(schema, level):
    properties = schema.get("properties")
    if not isinstance(properties, dict) or not properties:
        return "obj"

    entries = []
    for key, subschema in properties.items():
        value = convert(subschema, level + 1)
        if value is None:
            print(f"warning: dropping property {key!r} (no JSSN-representable type)", file=sys.stderr)
            continue
        entries.append(f"{key}: {value}")

    if not entries:
        return "obj"

    inner_indent = INDENT * (level + 1)
    close_indent = INDENT * level
    body = "\n".join(f"{inner_indent}{entry}" for entry in entries)
    return "{\n" + body + "\n" + close_indent + "}"


def convert_array(schema, level):
    prefix_items = schema.get("prefixItems")
    items = schema.get("items")

    if isinstance(prefix_items, list):
        item_schemas = prefix_items
    elif isinstance(items, list):
        item_schemas = items
    elif isinstance(items, dict):
        item_schemas = [items]
    else:
        item_schemas = None

    if not item_schemas:
        return "arr"

    values = []
    for subschema in item_schemas:
        value = convert(subschema, level + 1)
        if value is None:
            print("warning: dropping array item (no JSSN-representable type)", file=sys.stderr)
            continue
        values.append(value)

    if not values:
        return "arr"

    inner_indent = INDENT * (level + 1)
    close_indent = INDENT * level
    body = "\n".join(f"{inner_indent}{value}" for value in values)
    return "[\n" + body + "\n" + close_indent + "]"


def main():
    parser = argparse.ArgumentParser(description="Convert a JSON Schema file to JSSN")
    parser.add_argument("input", help="path to the JSON Schema file")
    parser.add_argument("-o", "--output", help="path to write the JSSN output (defaults to stdout)")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        schema = json.load(f)

    jssn = convert(schema)
    if jssn is None:
        print("error: could not determine a JSSN-representable type for the root schema", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(jssn + "\n")
    else:
        print(jssn)


if __name__ == "__main__":
    main()
