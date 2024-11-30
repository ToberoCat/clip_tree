"""
Module: pysetup
Description: Contains the setup configuration for the clip_tree package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clip_tree",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyperclip~=1.9.0",
        "pathspec~=0.12.1"
    ],
    entry_points={
        "console_scripts": [
            "clip_tree=clip_tree.cli:main",
        ],
    },
    author="Tobero",
    url="https://github.com/ToberoCat/clip_tree",
    author_email="tobias.madlberger@gmail.com",
    description="A tool that copies folder and file structures "
                "to your clipboard for easy pasting into your ai interface of choice.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["clipboard", "directory structure", "CLI", "utility", "chatgpt"],
    project_urls={
        "Bug Reports": "https://github.com/ToberoCat/clip_tree/issues",
        "Documentation": "https://github.com/ToberoCat/clip_tree#readme",
        "Source": "https://github.com/ToberoCat/clip_tree",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="GNU",
    python_requires='>=3.6',
)
