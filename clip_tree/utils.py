"""
Module: utils
Description: Contains utility functions for the clip_tree package.
"""

from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)

def read_files_contents(files: List[Path], base_path: Path) -> str:
    """
    Reads the contents of the given files and formats them with tag names.

    Args:
        files (List[Path]): A list of file paths to read.
        base_path (Path): The base directory path for relative references.

    Returns:
        str: A concatenated string of file contents with tags.
    """
    contents = []
    for file in files:
        try:
            relative_path = file.relative_to(base_path)
            tag_name = str(relative_path).replace('\\', '/')
        except ValueError:
            tag_name = str(file.resolve()).replace('\\', '/')
        try:
            with file.open('r', encoding='utf-8') as f:
                file_content = f.read()
                contents.append(f"<{tag_name}>\n{file_content}\n</{tag_name}>")
        except (IOError, OSError) as e:
            logger.error(f"Error reading {file}: {e}")
    return "\n\n".join(contents)
