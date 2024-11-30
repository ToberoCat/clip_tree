from pathlib import Path
from typing import List

import pathspec

DEFAULT_IGNORES = {'.git', '.idea', '__pycache__'}


class IgnoreManager:
    def __init__(self, paths: List[str]):
        self.paths = paths
        self.ignore_spec = self.build_ignore_spec()

    def load_gitignore_patterns(self, path: Path) -> List[str]:
        gitignore_file = path / '.gitignore'
        patterns = []
        if gitignore_file.exists():
            with gitignore_file.open('r', encoding='utf-8') as f:
                patterns = f.read().splitlines()
        return patterns

    def build_ignore_spec(self) -> pathspec.PathSpec:
        all_patterns = [f'/{ignore}/' for ignore in DEFAULT_IGNORES]
        for path_str in self.paths:
            path = Path(path_str).resolve()
            if path.is_dir():
                for gitignore in path.rglob('.gitignore'):
                    gitignore_dir = gitignore.parent
                    patterns = self.load_gitignore_patterns(gitignore_dir)
                    for pattern in patterns:
                        if pattern.strip() and not pattern.strip().startswith('#'):
                            relative_pattern = str(
                                gitignore_dir.relative_to(path)) + '/' + pattern if gitignore_dir != path else pattern
                            all_patterns.append(relative_pattern)
            elif path.is_file():
                patterns = self.load_gitignore_patterns(path.parent)
                for pattern in patterns:
                    if pattern.strip() and not pattern.strip().startswith('#'):
                        all_patterns.append(pattern)
        return pathspec.PathSpec.from_lines('gitwildmatch', all_patterns)

    def is_ignored(self, file_path: Path) -> bool:
        try:
            relative_path = file_path.resolve().relative_to(Path.cwd())
            return self.ignore_spec.match_file(str(relative_path))
        except ValueError:
            return self.ignore_spec.match_file(str(file_path.resolve()))
