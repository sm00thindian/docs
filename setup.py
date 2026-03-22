"""
Setup configuration for the project.

This script contains information about the packages required,
versioning, and metadata for the package.
"""

from setuptools import setup, find_packages

setup(
    name='rag-document-optimizer',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'python-docx>=1.1.2',
        'nltk>=3.8.1',
    ],
)