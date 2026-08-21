# Converter

A JSON Schema → JSSN converter. It implements the syntax covered by JSSN spec [0.1.0](../spec/CHANGELOG.md#010---2026-08-16) — see [spec/](../spec/) for the full spec and [CHANGELOG.md](./CHANGELOG.md) for which spec version the converter currently tracks. See the [project README](../README.md) for an overview of JSSN.

## Usage

```sh
python3 json_schema_to_jssn.py <input.json> [-o <output.jssn>]
```

Reads a JSON Schema file and prints the equivalent JSSN to stdout, or writes it to a file when `-o`/`--output` is given.

## Supported Constructs

Only constructs currently defined in the spec are converted:

- `type` (`string`, `number`, `integer`, `boolean`, `object`, `array`, `null`)
- `properties`, for objects
- `items` / `prefixItems`, for arrays (`prefixItems` takes precedence when both are present)

Everything else — `$ref`, `allOf`/`anyOf`/`oneOf`, `enum`, `const`, `required`, `format`, `additionalProperties`, `default`, etc. — is silently dropped from the output, since it isn't part of the JSSN spec yet. A warning is printed to stderr for each property or array item that ends up with no JSSN-representable type.

See [examples/](../examples/) for sample input/output pairs, including one that shows dropped keywords (`with-unsupported.*`).

## Tests

```sh
python3 -m unittest discover -s tests
```

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for notable changes to the converter.
