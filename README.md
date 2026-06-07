# zotero_pdf_FullText

A lightweight utility that extracts the full text of PDFs attached to Zotero items and generates an analysis-ready CSV dataset.

The script reads a Zotero CSV export, locates attached PDF files, extracts their text using PyMuPDF, and creates an enriched CSV containing both bibliographic metadata and full-text content.

This is particularly useful for researchers who want to perform text mining, corpus analysis, topic modeling, Retrieval-Augmented Generation (RAG), or LLM-based analysis on their Zotero collections.

---

## Features

* Extracts full text from PDFs linked to Zotero items
* Preserves key bibliographic metadata
* Automatically calculates word counts
* Splits books into manageable chunks for downstream LLM processing
* Produces a clean, analysis-ready CSV dataset
* Simple command-line interface

---

## Installation

Clone the repository:

```bash
git clone https://github.com/rajabzadehalidip/zotero_pdf_FullText.git
cd zotero_pdf_FullText
```

Install dependencies:

```bash
pip install pymupdf
```

---

## Usage

Export a Zotero collection as a CSV file and run:

```bash
python enrich_zotero.py input.csv output.csv
```

Example:

```bash
python enrich_zotero.py my_library.csv my_library_fulltext.csv
```

If no output file is specified, the script creates:

```text
Importants_with_text.csv
```

---

## Typical Workflow

```text
Zotero Collection
        ↓
    Export CSV
        ↓
zotero_pdf_FullText
        ↓
  Enriched CSV
        ↓
NLP / Text Mining / RAG / LLM Analysis
```

---

## Output Schema

The generated CSV contains the following columns:

| Column     | Description                           |
| ---------- | ------------------------------------- |
| Title      | Title of the item                     |
| Authors    | Author(s)                             |
| DOI        | DOI identifier                        |
| URL        | URL associated with the item          |
| Abstract   | Abstract from Zotero                  |
| Full Text  | Extracted PDF text                    |
| Word Count | Number of words in the extracted text |

---

## Book Chunking

Books are often too large for efficient processing by LLMs and text-analysis pipelines.

To address this, items with `Item Type = book` are automatically split into chunks of 30 pages.

For example:

| Title              |
| ------------------ |
| My Book (part 1/4) |
| My Book (part 2/4) |
| My Book (part 3/4) |
| My Book (part 4/4) |

Each chunk becomes a separate row in the output dataset.

---

## Requirements

The script expects a Zotero CSV export containing the following fields:

* Title
* Author
* DOI
* URL
* Abstract Note
* Item Type
* File Attachments

Most importantly, the **File Attachments** field must contain accessible paths to local PDF files.

---

## Important Notes

### PDF Attachments Only

Only items with PDF attachments are processed.

Items without PDFs are skipped automatically.

### First PDF Only

If an item contains multiple PDF attachments, only the first PDF is processed.

### Accessible File Paths Required

The script reads PDFs directly from the file paths stored in the Zotero export.

If a PDF has been moved, deleted, or is inaccessible, the item will be skipped.

### PDF Quality Matters

The quality of extracted text depends on the PDF itself.

Scanned PDFs without OCR may produce incomplete or poor-quality text.

---

## Example Use Cases

* Literature review automation
* Corpus creation from Zotero libraries
* Topic modeling
* Content analysis
* Retrieval-Augmented Generation (RAG)
* Research knowledge-base construction
* LLM-assisted paper analysis

---

## Integration with LLMR

The output of this tool can be used directly with the LLMR package to analyze large collections of academic papers and research documents.

LLMR Repository:

https://github.com/asanaei/LLMR

---

## License

MIT License
