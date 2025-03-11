#!/usr/bin/env python
"""
Script de instalação para a Interface Docling
"""
from setuptools import setup, find_packages

setup(
    name="docling-interface",
    version="0.1.0",
    description="Interface gráfica para processamento de documentos com Docling",
    author="Docling Interface",
    packages=["docling_interface"] if not find_packages() else find_packages(),
    py_modules=["docling_interface", "run_interface", "start"],
    install_requires=[
        "docling>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "docling-interface=start:main",
            "docling-gui=start:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: General",
    ],
) 