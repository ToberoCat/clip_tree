"""
Module: tree_builder
Description: Builds a visual tree representation of the file system.
"""

from pathlib import Path
from typing import List
from .ignore_manager import IgnoreManager

class TreeBuilder:
    """
    Builds a visual tree representation of the file system.
    """
    def __init__(self, paths: List[str], recursive: bool, ignore_manager: IgnoreManager):
        """
        Initializes the TreeBuilder.

        Args:
            paths (List[str]): List of file or directory paths to build the tree from.
            recursive (bool): Whether to build the tree recursively.
            ignore_manager (IgnoreManager): Instance to check ignore patterns.
        """
        self.paths = paths
        self.recursive = recursive
        self.ignore_manager = ignore_manager

    def generate_tree(self) -> str:
        """
        Generates the tree structure as a string.

        Returns:
            str: The tree structure.
        """
        tree_lines = []
        for path_str in self.paths:
            path = Path(path_str).resolve()
            if path.is_dir():
                tree_lines.append(f"{path.name}/")
                tree_lines.extend(self.build_tree(path, prefix="    "))
            elif path.is_file():
                tree_lines.append(f"{path.name}")
        return "\n".join(tree_lines)

    def build_tree(self, directory: Path, prefix: str = "") -> List[str]:
        """
        Recursively builds the tree lines for a directory.

        Args:
            directory (Path): The directory to build the tree from.
            prefix (str): The prefix for the current level in the tree.

        Returns:
            List[str]: A list of tree lines.
        """
        tree = []
        try:
            entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            tree.append(f"{prefix}Permission Denied")
            return tree

        entries = [entry for entry in entries if not self.ignore_manager.is_ignored(entry)]

        for index, entry in enumerate(entries):
            connector = "├── " if index < len(entries) - 1 else "└── "
            if entry.is_dir() and self.recursive:
                tree.append(f"{prefix}{connector}{entry.name}/")
                extension = "│   " if index < len(entries) - 1 else "    "
                tree.extend(self.build_tree(entry, prefix=prefix + extension))
            elif entry.is_file():
                tree.append(f"{prefix}{connector}{entry.name}")
        return tree
