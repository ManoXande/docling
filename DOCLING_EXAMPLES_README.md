# Docling Example Scripts

This folder contains example scripts to help you get started with Docling, a powerful document processing library.

## Prerequisites

Make sure you have Docling installed:

```bash
pip install docling
```

## Available Scripts

### 1. Single Document Processing (`docling_example.py`)

This script processes a single document and demonstrates different ways to work with the Docling output.

**Usage:**
```bash
python docling_example.py path/to/document.pdf
```

or with a URL:

```bash
python docling_example.py https://arxiv.org/pdf/2408.09869
```

**What it does:**
- Converts the document
- Shows basic document information
- Exports to Markdown, HTML, and JSON
- Saves outputs to files
- Analyzes document elements
- Extracts sample text

### 2. Batch Document Processing (`docling_batch.py`)

This script processes multiple documents in a directory and saves the output in various formats.

**Usage:**
```bash
python docling_batch.py path/to/documents [output_directory]
```

**What it does:**
- Scans a directory for supported document types
- Processes each document
- Saves each document as Markdown, HTML, and JSON
- Provides a summary of the processing results

## Supported Document Types

Docling supports multiple document formats, including:
- PDF
- DOCX
- XLSX
- HTML
- PPTX
- TXT
- Images (PNG, JPG, JPEG)

## Example Workflow

1. Install Docling:
   ```bash
   pip install docling
   ```

2. Process a single document:
   ```bash
   python docling_example.py sample.pdf
   ```

3. Process a folder of documents:
   ```bash
   python docling_batch.py ./documents ./processed
   ```

4. Examine the outputs:
   - `output.md` (Markdown format)
   - `output.html` (HTML format)
   - `output.json` (JSON format)

## Troubleshooting

If you encounter any issues:

1. Make sure you have the latest version of Docling:
   ```bash
   pip install --upgrade docling
   ```

2. Check the [official Docling documentation](https://ds4sd.github.io/docling/).

3. For specific errors, refer to the error messages in the console output.

## Further Resources

- [Docling Documentation](https://ds4sd.github.io/docling/)
- [GitHub Repository](https://github.com/DS4SD/docling)
- [Technical Report](https://arxiv.org/abs/2408.09869) 