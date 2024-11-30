from pathlib import Path
from typing import List
import mimetypes

def read_files_contents(files: List[Path], base_path: Path) -> str:
    contents = []
    for file in files:
        if not mimetypes.guess_type(file)[0].startswith('text'):
            print(f"Skipping binary file: {file}")
            continue

        try:
            relative_path = file.relative_to(base_path)
            tag_name = str(relative_path).replace('\\', '/')
        except ValueError:
            tag_name = str(file.resolve()).replace('\\', '/')
        try:
            with file.open('r', encoding='utf-8') as f:
                file_content = f.read()
                contents.append(f"<{tag_name}>\n{file_content}\n</{tag_name}>")
        except Exception as e:
            print(f"Error reading {file}: {e}")
    return "\n\n".join(contents)
