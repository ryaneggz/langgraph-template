import os
from setuptools import setup, find_packages
from pathlib import Path

# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = os.getenv("VERSION")

setup(
    name="ai-term",
    version=VERSION,
    author="Ryan Eggleston",
    author_email="ryaneggleston@promptengineers.ai",
    description="A powerful CLI tool for AI interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryaneggz/ai-term",
    packages=find_packages(include=['src', 'src.*']),
    package_data={
        'src': [
            'flows/*',
            'utils/*',
            'system/*',
            '*.py',
            '*.md',
            '*.txt',
            '.example.env'
        ]
    },
    include_package_data=True,  # This is important!
    entry_points={
        'console_scripts': [
            'ai=src.main:main',  # Updated to use src.main
        ],
    },
    install_requires=[
        'python-dotenv',
        'langgraph',
        'langchain_anthropic',
        'langchain_openai',
        'langchain-community',
        'langchain-experimental',
    ],
    setup_requires=[
        'setuptools',
        'wheel',
    ],
    extras_require={
        'dev': [
            'pytest',
            'black',
            'flake8',
            'twine',
            'build',
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
)