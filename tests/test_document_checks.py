"""Isolated fictional OOXML tests; no original medical or employee data."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from tools.check_reports import DocumentError, inspect_report

EXAMPLE_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:body><w:p><w:r><w:t>Fictional example</w:t></w:r></w:p></w:body>'
    '</w:document>'
)


class WordPackageTests(unittest.TestCase):
    def make_docx(
        self, directory: str, *, content: str = EXAMPLE_XML, name: str = "sample.docx"
    ) -> Path:
        path = Path(directory) / name
        with ZipFile(path, "w") as archive:
            archive.writestr(
                "[Content_Types].xml",
                '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
            )
            archive.writestr("word/document.xml", content)
        return path

    def test_valid_document(self) -> None:
        with TemporaryDirectory() as directory:
            result = inspect_report(self.make_docx(directory))
            self.assertEqual(result["text_paragraphs"], 1)
            self.assertEqual(result["media_files"], 0)

    def test_missing_file(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaisesRegex(DocumentError, "Missing"):
                inspect_report(Path(directory) / "not-found.docx")

    def test_wrong_extension(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaisesRegex(DocumentError, "Expected a .docx"):
                inspect_report(self.make_docx(directory, name="not-word.zip"))

    def test_no_text_paragraphs(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaisesRegex(DocumentError, "No text paragraphs"):
                inspect_report(
                    self.make_docx(
                        directory, content=EXAMPLE_XML.replace("Fictional example", "")
                    )
                )

    def test_traversal_entry_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            path = self.make_docx(directory)
            with ZipFile(path, "a") as archive:
                archive.writestr("../secrets.txt", "fictional")
            with self.assertRaisesRegex(DocumentError, "Invalid DOCX member path"):
                inspect_report(path)

    def test_missing_document_xml(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "missing-xml.docx"
            with ZipFile(path, "w") as archive:
                archive.writestr("[Content_Types].xml", "<Types/>")
            with self.assertRaisesRegex(DocumentError, "Missing required"):
                inspect_report(path)
