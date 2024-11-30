#!/usr/bin/env python3
"""
Module: cli
Description: Command-line interface for the clip_tree tool.
"""

import argparse
import sys
from pathlib import Path
import pyperclip

from .ignore_manager import IgnoreManager
from .file_processor import FileProcessor
from .tree_builder import TreeBuilder
from .utils import read_files_contents

def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
        Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="A tool that copies folder and file structures"
                    " to your clipboard for easy pasting."
    )
    parser.add_argument(
        'paths',
        metavar='PATH',
        type=str,
        nargs='+',
        help='List of files or directories to copy contents from.'
    )
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Recursively process directories.'
    )
    parser.add_argument(
        '-i', '--instruction',
        type=str,
        default="",
        help='Custom instruction to include in the clipboard content.'
    )
    parser.add_argument(
        '-e', '--exclude',
        metavar='PATTERN',
        type=str,
        nargs='*',
        default=[],
        help='Patterns to manually exclude (in addition to .gitignore patterns).'
    )
    return parser.parse_args()

def main():
    """
    The main entry point for the command-line interface.
    """
    args = parse_arguments()
    base_path = Path.cwd()

    ignore_manager = IgnoreManager(args.paths, manual_excludes=args.exclude)
    file_processor = FileProcessor(args.paths, args.recursive, ignore_manager)

    files = file_processor.get_all_files()
    if not files:
        print("No valid files to copy.", file=sys.stderr)
        sys.exit(1)

    tree_builder = TreeBuilder(args.paths, args.recursive, ignore_manager)
    tree_structure = tree_builder.generate_tree()

    combined_content = read_files_contents(files, base_path)

    clipboard_content = ""
    if args.instruction:
        clipboard_content += f"<instruction>{args.instruction}</instruction>\n\n"

    if tree_structure:
        clipboard_content += f"<fileTree>\n{tree_structure}\n</fileTree>\n\n"

    if combined_content:
        clipboard_content += combined_content

    if clipboard_content:
        try:
            pyperclip.copy(clipboard_content)
            print("Contents copied to clipboard successfully.")
        except pyperclip.PyperclipException as e:
            print(f"Failed to copy to clipboard: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("No content to copy.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
