"""
Module: file_processor
Description: Processes files and directories,
applying to ignore patterns and collecting files to be processed.
"""

import sys
from pathlib import Path
from typing import List
from .ignore_manager import IgnoreManager


class FileProcessor:
    """
    Processes files and directories to collect a list of files, considering ignore patterns.
    """

    def __init__(self, paths: List[str], recursive: bool, ignore_manager: IgnoreManager):
        """
        Initializes the FileProcessor.

        Args:
            paths (List[str]): List of file or directory paths to process.
            recursive (bool): Whether to process directories recursively.
            ignore_manager (IgnoreManager): Instance to check ignore patterns.
        """
        self.paths = paths
        self.recursive = recursive
        self.ignore_manager = ignore_manager

    def get_all_files(self) -> List[Path]:
        """
        Collects all files from the provided paths, considering ignore patterns.

        Returns:
            List[Path]: A list of file paths.
        """
        all_files = []
        for path_str in self.paths:
            path = Path(path_str)
            if not path.exists():
                print(f"Warning: {path} does not exist and will be skipped.", file=sys.stderr)
                continue
            if path.is_file():
                if not self.ignore_manager.is_ignored(path):
                    all_files.append(path.resolve())
            elif path.is_dir():
                all_files.extend(self.process_directory(path))
            else:
                print(f"Warning: {path} is neither a"
                      f" file nor a directory and will be skipped.", file=sys.stderr)
        return all_files

    def process_directory(self, directory: Path) -> List[Path]:
        """
        Processes a directory to collect files, considering ignore patterns.

        Args:
            directory (Path): The directory path to process.

        Returns:
            List[Path]: A list of file paths from the directory.
        """
        files = []
        if self.recursive:
            for file in directory.rglob('*'):
                if file.is_file() and not self.ignore_manager.is_ignored(file):
                    files.append(file.resolve())
        else:
            for file in directory.iterdir():
                if file.is_file() and not self.ignore_manager.is_ignored(file):
                    files.append(file.resolve())
        return files
