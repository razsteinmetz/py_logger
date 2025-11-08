"""
Setup script for PyLogger package.
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="py-logger-advanced",
    version="1.0.0",
    author="Raz Steinmetz",
    author_email="raz.steinmetz@gmail.com",
    description="A comprehensive Python logging package with multiple notification destinations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/py-logger",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/py-logger/issues",
        "Documentation": "https://github.com/yourusername/py-logger#readme",
        "Source Code": "https://github.com/yourusername/py-logger",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    keywords="logging, notifications, telegram, pushover, email, alerts, monitoring",
    include_package_data=True,
    package_data={
        "py_logger": ["*.yaml", "*.yml"],
    },
    zip_safe=False,
)