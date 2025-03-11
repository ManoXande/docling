#!/usr/bin/env python
"""
Docling Batch Processing Script
------------------------------
This script demonstrates how to use Docling to process multiple documents in a directory.

Usage:
    python docling_batch.py [--help] [--output OUTPUT_DIR] INPUT_DIR
    
    # Example
    python docling_batch.py --output ./processed ./documents
"""

import os
import sys
import time
import argparse
from pathlib import Path
from docling.document_converter import DocumentConverter


def process_document(converter, file_path, output_dir):
    """Process a single document and save the results."""
    try:
        print(f"Processing: {file_path}")
        start_time = time.time()
        
        # Convert the document
        result = converter.convert(file_path)
        doc = result.document
        
        # Create output filenames based on the original filename
        base_name = Path(file_path).stem
        output_base = os.path.join(output_dir, base_name)
        
        # Save as markdown (safely handle potential errors)
        try:
            markdown = doc.export_to_markdown()
            with open(f"{output_base}.md", "w", encoding="utf-8") as f:
                f.write(markdown or "")
        except Exception as e:
            print(f"  Warning: Failed to export markdown: {e}")
            
        # Save as HTML (safely handle potential errors)
        try:
            html_output = getattr(doc, 'export_to_html', lambda: "")()
            with open(f"{output_base}.html", "w", encoding="utf-8") as f:
                f.write(html_output or "")
        except Exception as e:
            print(f"  Warning: Failed to export HTML: {e}")
            
        # Save as JSON (safely handle potential errors)
        try:
            json_output = getattr(doc, 'export_to_json', lambda: "{}")()
            with open(f"{output_base}.json", "w", encoding="utf-8") as f:
                f.write(json_output or "{}")
        except Exception as e:
            print(f"  Warning: Failed to export JSON: {e}")
        
        duration = time.time() - start_time
        print(f"✓ Completed in {duration:.2f} seconds. Output saved to {output_base}.*")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process multiple documents using Docling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "input_dir",
        nargs="?", 
        help="Directory containing documents to process"
    )
    
    parser.add_argument(
        "--output", "-o",
        dest="output_dir",
        default="docling_output",
        help="Directory to save processed documents (default: docling_output)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if input_dir was provided
    if not args.input_dir:
        parser.print_help()
        return 1
    
    input_dir = args.input_dir
    output_dir = args.output_dir
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a valid directory")
        return 1
    
    # Initialize the converter
    converter = DocumentConverter()
    
    # Find supported documents
    supported_extensions = ['.pdf', '.docx', '.xlsx', '.html', '.pptx', '.txt', '.png', '.jpg', '.jpeg']
    documents = []
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_extensions:
                documents.append(os.path.join(root, file))
    
    # Process all documents
    if not documents:
        print(f"No supported documents found in {input_dir}")
        return 0
    
    print(f"Found {len(documents)} documents to process")
    
    successful = 0
    failed = 0
    
    for doc_path in documents:
        if process_document(converter, doc_path, output_dir):
            successful += 1
        else:
            failed += 1
    
    print("\n===== Processing Summary =====")
    print(f"Total documents: {len(documents)}")
    print(f"Successfully processed: {successful}")
    print(f"Failed: {failed}")
    print(f"Output saved to: {os.path.abspath(output_dir)}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main()) 