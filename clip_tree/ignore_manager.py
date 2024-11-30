"""
Module: ignore_manager
Description: Manages ignore patterns for files and directories, including .gitignore files and manual exclusions.
"""

from pathlib import Path
from typing import List
import pathspec

DEFAULT_IGNORES = {'.git', '.idea', '__pycache__'}

class IgnoreManager:
    """
    Manages ignore patterns for files and directories.
    """
    def __init__(self, paths: List[str], manual_excludes: List[str] = None):
        """
        Initializes the IgnoreManager with paths and optional manual exclusions.

        Args:
            paths (List[str]): List of paths to process.
            manual_excludes (List[str], optional): List of manual exclude patterns.
        """
        self.paths = paths
        self.manual_excludes = manual_excludes if manual_excludes else []
        self.ignore_spec = self.build_ignore_spec()

    def load_gitignore_patterns(self, path: Path) -> List[str]:
        """
        Loads patterns from a .gitignore file in the given path.

        Args:
            path (Path): The directory path containing the .gitignore file.

        Returns:
            List[str]: A list of patterns from the .gitignore file.
        """
        gitignore_file = path / '.gitignore'
        patterns = []
        if gitignore_file.exists():
            with gitignore_file.open('r', encoding='utf-8') as f:
                patterns = f.read().splitlines()
        return patterns

    def build_ignore_spec(self) -> pathspec.PathSpec:
        """
        Builds the ignore specification from default ignores, .gitignore files, and manual excludes.

        Returns:
            pathspec.PathSpec: The compiled ignore specification.
        """
        all_patterns = [f'/{ignore}/' for ignore in DEFAULT_IGNORES]
        all_patterns.extend(self.manual_excludes)
        for path_str in self.paths:
            path = Path(path_str).resolve()
            if path.is_dir():
                for gitignore in path.rglob('.gitignore'):
                    gitignore_dir = gitignore.parent
                    patterns = self.load_gitignore_patterns(gitignore_dir)
                    for pattern in patterns:
                        pattern = pattern.strip()
                        if pattern and not pattern.startswith('#'):
                            relative_pattern = (
                                f"{gitignore_dir.relative_to(path)}/{pattern}"
                                if gitignore_dir != path else pattern
                            )
                            all_patterns.append(relative_pattern)
            elif path.is_file():
                patterns = self.load_gitignore_patterns(path.parent)
                for pattern in patterns:
                    pattern = pattern.strip()
                    if pattern and not pattern.startswith('#'):
                        all_patterns.append(pattern)
        return pathspec.PathSpec.from_lines('gitwildmatch', all_patterns)

    def is_ignored(self, file_path: Path) -> bool:
        """
        Checks if a file path should be ignored based on the ignore specification.

        Args:
            file_path (Path): The file path to check.

        Returns:
            bool: True if the file should be ignored, False otherwise.
        """
        try:
            relative_path = file_path.resolve().relative_to(Path.cwd())
            return self.ignore_spec.match_file(str(relative_path))
        except ValueError:
            return self.ignore_spec.match_file(str(file_path.resolve()))