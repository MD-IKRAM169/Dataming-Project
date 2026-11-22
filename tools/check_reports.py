#!/usr/bin/env python3
"""Read-only OOXML integrity checks for historical Word reports.

Does not extract files, print report text, execute macros or establish scientific
correctness. Uses only Python's standard library.
"""
from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import stat
import sys
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile

MAX_MEMBERS = 1000
MAX_XML_BYTES = 12 * 1024 * 1024
MAX_ARCHIVE_UNCOMPRESSED_BYTES = 32 * 1024 * 1024
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


class DocumentError(ValueError):
    """Invalid Word document package or unsafe archive member."""


def inspect_report(path: Path) -> dict[str, object]:
    path = Path(path)
    if not path.is_file():
        raise DocumentError(f"Missing document: {path}")
    if path.suffix.lower() != ".docx":
        raise DocumentError(f"Expected a .docx file: {path.name}")
    try:
        with ZipFile(path) as archive:
            infos = archive.infolist()
            if not infos or len(infos) > MAX_MEMBERS:
                raise DocumentError("Document member count exceeds safety limit")
            names: set[str] = set()
            uncompressed_bytes = 0
            for member in infos:
                name = member.filename
                parsed = PurePosixPath(name)
                if (
                    not name or name.startswith("/") or "\\" in name or
                    "\x00" in name or parsed.is_absolute() or
                    ".." in parsed.parts or
                    (len(name) >= 2 and name[1] == ":")
                ):
                    raise DocumentError("Invalid DOCX member path")
                if name in names:
                    raise DocumentError("Duplicate DOCX member path")
                names.add(name)
                if member.flag_bits & 1:
                    raise DocumentError("Encrypted DOCX member")
                if stat.S_IFMT(member.external_attr >> 16) == stat.S_IFLNK:
                    raise DocumentError("Symlink DOCX member")
                uncompressed_bytes += member.file_size
                if uncompressed_bytes > MAX_ARCHIVE_UNCOMPRESSED_BYTES:
                    raise DocumentError("DOCX exceeds uncompressed size limit")
                if name.lower().endswith("vbaproject.bin"):
                    raise DocumentError("Macro-enabled Word documents are not allowed")
            required = {"[Content_Types].xml", "word/document.xml"}
            if not required.issubset(names):
                raise DocumentError("Missing required DOCX package entries")
            info = archive.getinfo("word/document.xml")
            if info.file_size > MAX_XML_BYTES:
                raise DocumentError("Word XML exceeds size limit")
            document_xml = archive.read(info)
            root = ET.fromstring(document_xml)
            paragraphs = root.findall(f".//{W_NS}p")
            text_paragraphs = sum(
                bool(
                    any((run.text or "").strip() for run in p.findall(f".//{W_NS}t"))
                ) for p in paragraphs
            )
            if not text_paragraphs:
                raise DocumentError("No text paragraphs in DOCX")
            media_count = sum(
                1 for name in names
                if name.startswith("word/media/") and not name.endswith("/")
            )
    except (BadZipFile, OSError, ET.ParseError, RuntimeError, EOFError, NotImplementedError) as exc:
        raise DocumentError(f"Cannot inspect document package: {exc}") from exc
    return {
        "file": path.name,
        "text_paragraphs": text_paragraphs,
        "media_files": media_count,
        "archive_bytes": path.stat().st_size,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", type=Path, nargs="+", help="DOCX files to check")
    args = parser.parse_args(argv)
    try:
        for report in args.reports:
            result = inspect_report(report)
            print(
                f"OK {result['file']}: {result['text_paragraphs']} nonempty paragraphs, "
                f"{result['media_files']} embedded media file(s)"
            )
    except DocumentError as exc:
        print(f"DOCX check FAILED: {exc}", file=sys.stderr)
        return 1
    print("Structure checked; original scholarly findings not assessed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
