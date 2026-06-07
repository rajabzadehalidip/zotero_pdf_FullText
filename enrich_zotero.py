#!/usr/bin/env python3
"""Read a Zotero CSV, extract full text from linked PDFs, and write enriched CSV.

Usage:
    python3 enrich_zotero.py Importants.csv [Importants_with_text.csv]
"""

import csv
import os
import sys

import fitz  # PyMuPDF — pip install pymupdf

BOOK_PAGE_CHUNK = 30


def extract_page_texts(pdf_path: str) -> list[str] | None:
    if not pdf_path or not os.path.exists(pdf_path):
        return None
    try:
        doc = fitz.open(pdf_path)
        page_texts = [page.get_text().strip() for page in doc]
        doc.close()
        return page_texts
    except Exception as e:
        print(f"  ERROR reading {pdf_path}: {e}", file=sys.stderr)
        return None


def split_into_chunks(page_texts: list[str], chunk_size: int) -> list[str]:
    chunks = []
    for i in range(0, len(page_texts), chunk_size):
        chunk = "\n\n".join(page_texts[i:i + chunk_size]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <zotero_csv_path> [output_csv_path]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "Importants_with_text.csv"

    with open(input_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    output_rows = []
    for r in rows:
        item_type = r.get("Item Type", "")
        title = r.get("Title", "").strip()
        authors = r.get("Author", "").strip()
        doi = r.get("DOI", "").strip()
        url = r.get("Url", "").strip()
        abstract = r.get("Abstract Note", "").strip()

        fa = r.get("File Attachments", "").strip()
        pdf_path = None
        if fa:
            for part in fa.split(";"):
                part = part.strip()
                if part.lower().endswith(".pdf"):
                    pdf_path = part
                    break

        page_texts = extract_page_texts(pdf_path) if pdf_path else None
        if not page_texts:
            continue

        if item_type == "book":
            chunks = split_into_chunks(page_texts, BOOK_PAGE_CHUNK)
            for i, chunk_text in enumerate(chunks, 1):
                output_rows.append({
                    "Title": f"{title} (part {i}/{len(chunks)})",
                    "Authors": authors,
                    "DOI": doi,
                    "URL": url,
                    "Abstract": abstract,
                    "Full Text": chunk_text,
                    "Word Count": len(chunk_text.split()),
                })
        else:
            full = "\n\n".join(page_texts).strip()
            output_rows.append({
                "Title": title,
                "Authors": authors,
                "DOI": doi,
                "URL": url,
                "Abstract": abstract,
                "Full Text": full,
                "Word Count": len(full.split()),
            })

    out_fields = ["Title", "Authors", "DOI", "URL", "Abstract", "Full Text", "Word Count"]
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Done — {len(output_rows)} rows written to {output_path}")


if __name__ == "__main__":
    main()
