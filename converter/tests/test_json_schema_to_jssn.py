import contextlib
import io
import json
import os
import subprocess
import sys
import unittest

CONVERTER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(CONVERTER_DIR)
EXAMPLES_DIR = os.path.join(REPO_ROOT, "examples")

sys.path.insert(0, CONVERTER_DIR)
import json_schema_to_jssn as converter


def load_example(name):
    with open(os.path.join(EXAMPLES_DIR, f"{name}.schema.json"), encoding="utf-8") as f:
        schema = json.load(f)
    with open(os.path.join(EXAMPLES_DIR, f"{name}.jssn"), encoding="utf-8") as f:
        expected = f.read().rstrip("\n")
    return schema, expected


class ExampleFixturesTest(unittest.TestCase):
    def test_supported_example_converts_without_dropping_anything(self):
        schema, expected = load_example("supported")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = converter.convert(schema)
        self.assertEqual(result, expected)
        self.assertEqual(stderr.getvalue(), "", "fully-supported example should not warn")

    def test_with_unsupported_example_drops_unsupported_parts(self):
        schema, expected = load_example("with-unsupported")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = converter.convert(schema)
        self.assertEqual(result, expected)
        warnings = stderr.getvalue()
        self.assertIn("settings", warnings)
        self.assertIn("dropping array item", warnings)
        # Keywords not yet part of the JSSN spec must not leak into the output.
        for keyword in (
            "required",
            "additionalProperties",
            "format",
            "enum",
            "$ref",
            "anyOf",
            "default",
        ):
            self.assertNotIn(keyword, result)


class TypeAliasTest(unittest.TestCase):
    def test_primitive_aliases(self):
        for json_type, alias in converter.TYPE_ALIASES.items():
            self.assertEqual(converter.convert({"type": json_type}), alias)

    def test_unknown_type_is_unsupported(self):
        self.assertIsNone(converter.convert({"type": "unknown"}))

    def test_union_type_picks_first_supported_member(self):
        self.assertEqual(converter.convert({"type": ["string", "null"]}), "str")

    def test_union_type_with_no_supported_member_is_unsupported(self):
        self.assertIsNone(converter.convert({"type": ["foo", "bar"]}))


class ObjectConversionTest(unittest.TestCase):
    def test_object_without_properties_is_generic_obj(self):
        self.assertEqual(converter.convert({"type": "object"}), "obj")

    def test_object_with_empty_properties_is_generic_obj(self):
        self.assertEqual(converter.convert({"type": "object", "properties": {}}), "obj")

    def test_type_is_inferred_from_properties(self):
        schema = {"properties": {"a": {"type": "string"}}}
        self.assertEqual(converter.convert(schema), "{\n  a: str\n}")

    def test_nested_object_indentation(self):
        schema = {
            "type": "object",
            "properties": {
                "outer": {
                    "type": "object",
                    "properties": {"inner": {"type": "integer"}},
                }
            },
        }
        expected = "{\n  outer: {\n    inner: int\n  }\n}"
        self.assertEqual(converter.convert(schema), expected)

    def test_property_with_no_representable_type_is_dropped(self):
        schema = {
            "type": "object",
            "properties": {
                "kept": {"type": "string"},
                "dropped": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
            },
        }
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = converter.convert(schema)
        self.assertEqual(result, "{\n  kept: str\n}")
        self.assertIn("dropped", stderr.getvalue())

    def test_object_with_only_unsupported_properties_is_generic_obj(self):
        schema = {"type": "object", "properties": {"a": {"$ref": "#/x"}}}
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(converter.convert(schema), "obj")


class ArrayConversionTest(unittest.TestCase):
    def test_array_without_items_is_generic_arr(self):
        self.assertEqual(converter.convert({"type": "array"}), "arr")

    def test_type_is_inferred_from_items(self):
        schema = {"items": {"type": "integer"}}
        self.assertEqual(converter.convert(schema), "[\n  int\n]")

    def test_homogeneous_items_produce_single_element_array(self):
        schema = {"type": "array", "items": {"type": "string"}}
        self.assertEqual(converter.convert(schema), "[\n  str\n]")

    def test_tuple_items_list_form(self):
        schema = {"type": "array", "items": [{"type": "string"}, {"type": "integer"}]}
        self.assertEqual(converter.convert(schema), "[\n  str\n  int\n]")

    def test_prefix_items_preferred_over_items(self):
        schema = {
            "type": "array",
            "prefixItems": [{"type": "number"}, {"type": "number"}],
            "items": False,
        }
        self.assertEqual(converter.convert(schema), "[\n  num\n  num\n]")

    def test_array_with_only_unsupported_item_is_generic_arr(self):
        schema = {"type": "array", "items": {"$ref": "#/x"}}
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(converter.convert(schema), "arr")


class CliTest(unittest.TestCase):
    def run_cli(self, *args):
        script = os.path.join(CONVERTER_DIR, "json_schema_to_jssn.py")
        return subprocess.run(
            [sys.executable, script, *args],
            capture_output=True,
            text=True,
        )

    def test_cli_prints_to_stdout(self):
        path = os.path.join(EXAMPLES_DIR, "supported.schema.json")
        proc = self.run_cli(path)
        self.assertEqual(proc.returncode, 0)
        with open(os.path.join(EXAMPLES_DIR, "supported.jssn"), encoding="utf-8") as f:
            expected = f.read()
        self.assertEqual(proc.stdout, expected)

    def test_cli_errors_on_fully_unsupported_root_schema(self):
        with subprocess.Popen(
            [sys.executable, os.path.join(CONVERTER_DIR, "json_schema_to_jssn.py"), "/dev/stdin"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as proc:
            stdout, stderr = proc.communicate(json.dumps({"$ref": "#/x"}))
            self.assertEqual(proc.returncode, 1)
            self.assertIn("error", stderr)
            self.assertEqual(stdout, "")


if __name__ == "__main__":
    unittest.main()
