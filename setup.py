#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataForgePDF - Генератор PDF из файлов данных
Setup script для установки пакета
"""

from setuptools import setup, find_packages
import os

# Читаем README.md для описания
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Читаем requirements.txt для зависимостей
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dataforgepdf",
    version="1.0.0",
    author="DataForgePDF Team",
    author_email="",
    description="Генератор PDF документов с полной поддержкой кириллицы",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/DataForgePDF",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "dataforgepdf=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.ttf", "*.txt", "*.csv", "*.json"],
    },
    keywords="pdf generation, cyrillic support, data processing, weasyprint, reportlab",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/DataForgePDF/issues",
        "Source": "https://github.com/yourusername/DataForgePDF",
        "Documentation": "https://github.com/yourusername/DataForgePDF#readme",
    },
)
