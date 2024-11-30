# Clip Tree

Clip Tree is a handy tool that copies entire folder and file structures to your clipboard for easy pasting into platforms like ChatGPT.

## Features

- Recursively copy directory structures.
- Respect `.gitignore` patterns.
- Custom instructions can be added to the clipboard content.
- Configurable and easy to use.

## Installation

```bash
pip install clip_tree
```

## Usage

```bash
clip_tree path/to/directory -r -i "Your custom instruction"
```

- `-r`, `--recursive`: Recursively process directories.
- `-i`, `--instruction`: Custom instruction to include in the clipboard content.

## Example

Run this command in your terminal, for example in this project's root directory:

```bash
clip_tree -i "Please review my code." -r .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.