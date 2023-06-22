# jupyter-cleaner

jupyter-cleaner makes tracking Jupyter lab files in git easy.

This is done by:
- Removing output of all cells
- Formatting all cells (using black)
- Reordering imports in all cells (using reorder-python-imports)
- Setting the execution count of all cells
- pretty printing the lab file

It is recommended to run jupyter-cleaner using [pre-commit](https://pre-commit.com/):
```
default_language_version:
  python: python3.11
repos:
- repo: local
  hooks:
      - id: jupyter-cleaner
        name: jupyter-cleaner
        entry: jupyter-cleaner .
        language: system
        pass_filenames: false
        always_run: true
```

## CLI
running `jupyter-cleaner -h` displays:
```
usage: jupyter-cleaner [-h] [--exclude_files_or_dirs EXCLUDE_FILES_OR_DIRS [EXCLUDE_FILES_OR_DIRS ...]] [--execution_count EXECUTION_COUNT]
                       [--indent_level INDENT_LEVEL] [--remove_code_output] [--format] [--reorder_imports]
                       files_or_dirs [files_or_dirs ...]

jupyter_cleaner

positional arguments:
  files_or_dirs         Jupyter lab files to format or directories to search for lab files

options:
  -h, --help            show this help message and exit
  --exclude_files_or_dirs EXCLUDE_FILES_OR_DIRS [EXCLUDE_FILES_OR_DIRS ...]
                        Jupyter lab files or directories to exclude from formatting and search
  --execution_count EXECUTION_COUNT
                        Number to set for the execution count of every cell
  --indent_level INDENT_LEVEL
                        Integer greater than zero will pretty-print the JSON array with that indent level. An indent level of 0 or negative will only
                        insert newlines.
  --remove_code_output  Number to set for the execution count of every cell
  --format              Format code of every cell (uses black)
  --reorder_imports     Reorder imports of every cell (uses reorder-python-imports)
```

## pyproject.toml
Inputs to jupyter-cleaner can be supplied via pyproject.toml:
```
[tool.jupyter_cleaner]
execution_count=0
remove_code_output=true
format=true
reorder_imports=true
indent_level=4
```
