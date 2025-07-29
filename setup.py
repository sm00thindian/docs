# setup.py (optional, for pip install -e .)
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
