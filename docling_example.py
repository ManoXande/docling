#!/usr/bin/env python
"""
Docling Example Script
---------------------
This script demonstrates how to use Docling to convert and process documents.

Usage:
    python docling_example.py [--help] path/to/document.pdf
    
    # Or with a URL
    python docling_example.py https://arxiv.org/pdf/2408.09869
"""

import os
import sys
import argparse
from docling.document_converter import DocumentConverter


def process_document(document_path):
    """Process a document and show different ways to use the result."""
    print(f"Converting document: {document_path}")
    
    try:
        # Initialize the DocumentConverter
        converter = DocumentConverter()
        
        # Convert the document (local file or URL)
        result = converter.convert(document_path)
        
        # Access the parsed document
        doc = result.document
        
        # ----------------------------------------
        # Different ways to work with the document
        # ----------------------------------------
        
        # 1. Print basic information about the document
        print("\n=== Document Information ===")
        # Get document structure safely
        content_elements = getattr(doc, 'content', []) or []
        pages = getattr(doc, 'pages', []) or []
        
        print(f"Document structure: {type(doc).__name__}")
        print(f"Number of content elements: {len(content_elements)}")
        print(f"Number of pages: {len(pages)}")
        
        # 2. Export to markdown
        print("\n=== Markdown Output (first 500 chars) ===")
        markdown = doc.export_to_markdown()
        if markdown:
            print(markdown[:500] + "..." if len(markdown) > 500 else markdown)
        else:
            print("No markdown output available")
        
        # Save markdown to file
        markdown_file = "output.md"
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(markdown or "")
        print(f"\nFull markdown output saved to {markdown_file}")
        
        # 3. Export to HTML
        html_output = getattr(doc, 'export_to_html', lambda: "")()
        html_file = "output.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_output or "")
        print(f"HTML output saved to {html_file}")
        
        # 4. Export to JSON (for programmatic access)
        json_output = getattr(doc, 'export_to_json', lambda: "{}")()
        json_file = "output.json"
        with open(json_file, "w", encoding="utf-8") as f:
            f.write(json_output or "{}")
        print(f"JSON output saved to {json_file}")
        
        # 5. Document structure exploration
        print("\n=== Document Structure ===")
        # Print available attributes and methods on the document object
        doc_attrs = [attr for attr in dir(doc) if not attr.startswith('_')]
        print(f"Available document attributes and methods: {', '.join(doc_attrs[:10])}...")
        
        # 6. Text extraction example
        print("\n=== Document Text ===")
        # Try different ways to access document text
        text = ""
        if hasattr(doc, 'text'):
            text = doc.text
        elif hasattr(doc, 'content') and doc.content:
            # Try to get text from content elements
            text_parts = []
            for item in doc.content:
                if hasattr(item, 'text'):
                    text_parts.append(item.text)
            text = "\n".join(text_parts)
            
        if text:
            print(f"Document text (sample): {text[:200]}...")
        else:
            print("No text found in the document")
        
        print("\nProcessing completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error processing document: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process a document using Docling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "document_path", 
        nargs="?",
        help="Path to the document file or URL to process"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if document_path was provided
    if not args.document_path:
        parser.print_help()
        return 1
    
    # Process the document
    success = process_document(args.document_path)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 