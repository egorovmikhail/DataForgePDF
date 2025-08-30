#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for DataForgePDF
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dataforgepdf",
    version="1.0.0",
    author="DataForgePDF Team",
    description="Генератор PDF из файлов данных с поддержкой кириллицы",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "openpyxl>=3.1.0",
        "python-docx>=1.1.0",
        "weasyprint>=60.0",
        "jinja2>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dataforgepdf=src.main:main",
        ],
    },
)
