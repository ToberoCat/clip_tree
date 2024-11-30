import sys
from pathlib import Path
from typing import List
from .ignore_manager import IgnoreManager


class FileProcessor:
    def __init__(self, paths: List[str], recursive: bool, ignore_manager: IgnoreManager):
        self.paths = paths
        self.recursive = recursive
        self.ignore_manager = ignore_manager

    def get_all_files(self) -> List[Path]:
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
                all_files.extend(self._process_directory(path))
            else:
                print(f"Warning: {path} is neither a file nor a directory and will be skipped.", file=sys.stderr)
        return all_files

    def _process_directory(self, directory: Path) -> List[Path]:
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