from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
    
setup(
    name="keyauth",
    version="1.0.0",
    description="Keyauth.win API Wrapper for python3",
    long_description="Keyauth.win API Wrapper for python3",
    author="dropout",
    author_email="dropout@fbi.ac",
    url="https://github.com/dropout1337",
    install_requires=[
        "requests",
        "pywin32",
        "pycryptodome"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ]
)