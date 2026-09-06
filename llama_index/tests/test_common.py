"""Tests for the local, non-API LlamaCloud helpers."""

from __future__ import annotations

import json
import runpy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PyPDF2 import PdfReader, PdfWriter

SCRIPTS_DIRECTORY = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIRECTORY))

import common  # noqa: E402


class PageNumbersTests(unittest.TestCase):
    """Check page-range expansion."""

    def test_expands_single_pages_and_ranges(self) -> None:
        """Return all configured pages in their original order."""
        self.assertEqual(common.page_numbers("3,8,12-14"), [3, 8, 12, 13, 14])

    def test_maps_sample_pages_to_source_pages(self) -> None:
        """Translate sample page positions through the configured manifest."""
        source_pages = [3, 8, 9, 12]
        self.assertEqual(common.source_page_for_sample(1, source_pages), 3)
        self.assertEqual(common.source_page_for_sample(4, source_pages), 12)

    def test_rejects_sample_pages_outside_manifest(self) -> None:
        """Reject provenance that cannot be mapped to the original PDF."""
        with self.assertRaises(ValueError):
            common.source_page_for_sample(5, [3, 8, 9, 12])

    def test_normalizes_integral_api_page_numbers(self) -> None:
        """Accept integer-valued floats returned by structured extraction."""
        self.assertEqual(common.normalize_page_number(11.0, [11, 12]), 11)

    def test_rejects_invalid_api_page_numbers(self) -> None:
        """Reject non-integral and out-of-scope provenance values."""
        for value in (11.5, 15, "11", True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                common.normalize_page_number(value, [11, 12])


class SamplePdfTests(unittest.TestCase):
    """Check sample creation without contacting LlamaCloud."""

    def test_creates_sample_and_page_manifest(self) -> None:
        """Copy selected pages and preserve their source-page mapping."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.pdf"
            writer = PdfWriter()
            for _ in range(4):
                writer.add_blank_page(width=100, height=100)
            with source.open("wb") as source_file:
                writer.write(source_file)

            config = {
                "document": {
                    "id": "test_document",
                    "source_pdf": "source.pdf",
                    "target_pages": "2,4",
                    "sample_pdf": "output/sample.pdf",
                }
            }
            with patch.object(common, "ROOT", root):
                sample = common.ensure_sample(config)
                reused = common.ensure_sample(config)

            self.assertEqual(sample, reused)
            self.assertEqual(len(PdfReader(sample).pages), 2)
            manifest = json.loads((sample.parent / "page_manifest.json").read_text())
            self.assertEqual(
                manifest,
                [
                    {"sample_page": 1, "source_pdf_page": 2},
                    {"sample_page": 2, "source_pdf_page": 4},
                ],
            )


class ExperimentScriptTests(unittest.TestCase):
    """Check that every experiment loads without starting an API request."""

    def test_scripts_expose_main_functions(self) -> None:
        """Import each numbered script and find its guarded entry point."""
        script_paths = sorted(SCRIPTS_DIRECTORY.glob("[0-9][0-9]_*.py"))
        self.assertEqual(len(script_paths), 5)
        for script_path in script_paths:
            namespace = runpy.run_path(str(script_path), run_name="validation_only")
            self.assertTrue(callable(namespace.get("main")), script_path.name)

    def test_exports_native_parse_tables(self) -> None:
        """Preserve native CSV, rows, page numbers, and parse concerns."""
        namespace = runpy.run_path(
            str(SCRIPTS_DIRECTORY / "05_export_parse_tables.py"),
            run_name="validation_only",
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output_root = "output/full"
            raw_path = root / output_root / "parse_markdown/raw_result.json"
            raw_path.parent.mkdir(parents=True)
            raw_path.write_text(
                json.dumps(
                    {
                        "items": {
                            "pages": [
                                {
                                    "page_number": 7,
                                    "items": [
                                        {
                                            "type": "table",
                                            "csv": '"Class","Value"\n"Motor","12"',
                                            "rows": [["Class", "Value"], ["Motor", "12"]],
                                            "parse_concerns": [{"type": "test_concern"}],
                                        }
                                    ],
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )
            namespace["main"].__globals__["load_config"] = lambda: {
                "output": {"root": output_root}
            }
            namespace["main"].__globals__["log"] = lambda *args, **kwargs: None
            with patch.object(common, "ROOT", root):
                namespace["main"]()

            csv_path = root / output_root / "parse_tables/csv/page_007_table_01.csv"
            native_path = root / output_root / "parse_tables/native_rows.json"
            self.assertEqual(csv_path.read_text(), '"Class","Value"\n"Motor","12"\n')
            native_rows = json.loads(native_path.read_text())
            self.assertEqual(native_rows[0]["source_pdf_page"], 7)
            self.assertEqual(native_rows[0]["rows"][1], ["Motor", "12"])


if __name__ == "__main__":
    unittest.main()
