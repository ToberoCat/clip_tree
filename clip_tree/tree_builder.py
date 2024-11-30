from pathlib import Path
from typing import List

from .ignore_manager import IgnoreManager


class TreeBuilder:
    def __init__(self, paths: List[str], recursive: bool, ignore_manager: IgnoreManager):
        self.paths = paths
        self.recursive = recursive
        self.ignore_manager = ignore_manager

    def generate_tree(self) -> str:
        tree_lines = []
        for path_str in self.paths:
            path = Path(path_str).resolve()
            if path.is_dir():
                tree_lines.append(f"{path.name}/")
                tree_lines.extend(self._build_tree(path, prefix="    "))
            elif path.is_file():
                tree_lines.append(f"{path.name}")
        return "\n".join(tree_lines)

    def _build_tree(self, directory: Path, prefix: str = "") -> List[str]:
        tree = []
        try:
            entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            tree.append(f"{prefix}Permission Denied")
            return tree

        for index, entry in enumerate(entries):
            if self.ignore_manager.is_ignored(entry):
                continue
            connector = "├── " if index < len(entries) - 1 else "└── "
            if entry.is_dir() and self.recursive:
                tree.append(f"{prefix}{connector}{entry.name}/")
                extension = "│   " if index < len(entries) - 1 else "    "
                tree.extend(self._build_tree(entry, prefix=prefix + extension))
            elif entry.is_file():
                tree.append(f"{prefix}{connector}{entry.name}")
        return tree
