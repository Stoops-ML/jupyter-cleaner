import json
import os
import tempfile
from pathlib import Path
from typing import List

from jupyter_cleaner.jupyter_cleaner import get_lab_files  # type: ignore
from jupyter_cleaner.jupyter_cleaner import parse_pyproject  # type: ignore
from jupyter_cleaner.jupyter_cleaner import process_inputs  # type: ignore
from jupyter_cleaner.jupyter_cleaner import run  # type: ignore


def test_defaults() -> None:
    """Test run() with defaults"""
    data = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [
                    {
                        "data": {
                            "text/html": [
                                "\n",
                                '                <script type="application/javascript" id="jupyter_reorder_python_imports">\n',
                                "                (function() {\n",
                                "                    if (window.IPython === undefined) {\n",
                                "                        return\n",
                                "                    }\n",
                                '                    var msg = "WARNING: it looks like you might have loaded " +\n',
                                '                        "jupyter_reorder_python_imports in a non-lab notebook with " +\n',
                                '                        "`is_lab=True`. Please double check, and if " +\n',
                                '                        "loading with `%load_ext` please review the README!"\n',
                                "                    console.log(msg)\n",
                                "                    alert(msg)\n",
                                "                })()\n",
                                "                </script>\n",
                                "                ",
                            ],
                            "text/plain": ["<IPython.core.display.HTML object>"],
                        },
                        "metadata": {},
                        "output_type": "display_data",
                    }
                ],
                "source": [
                    "%load_ext jupyter_reorder_python_imports\n",
                    "%load_ext jupyter_black",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": 5,
                "metadata": {},
                "outputs": [],
                "source": ["import re\n", "import datetime"],
            },
            {
                "cell_type": "code",
                "execution_count": 10,
                "metadata": {},
                "outputs": [
                    {
                        "data": {"text/plain": ["1"]},
                        "execution_count": 4,
                        "metadata": {},
                        "output_type": "execute_result",
                    }
                ],
                "source": ["a=1\na"],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "jreorder-1i-52Iue",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.10",
            },
            "orig_nbformat": 4,
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }
    expected_result = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": "null",
                "metadata": {},
                "outputs": [],
                "source": [
                    "%load_ext jupyter_reorder_python_imports\n",
                    "%load_ext jupyter_black",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": "null",
                "metadata": {},
                "outputs": [],
                "source": ["import datetime\n", "import re"],
            },
            {
                "cell_type": "code",
                "execution_count": "null",
                "metadata": {},
                "outputs": [],
                "source": ["a = 1\n", "a"],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "jreorder-1i-52Iue",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.10",
            },
            "orig_nbformat": 4,
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    file = tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False)
    with open(file.name, "w") as f:
        json.dump(data, f)
    run([Path(file.name)])
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result


def test_inputs() -> None:
    """Test run() with defined inputs"""
    data = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [
                    {
                        "data": {
                            "text/html": [
                                "\n",
                                '                <script type="application/javascript" id="jupyter_reorder_python_imports">\n',
                                "                (function() {\n",
                                "                    if (window.IPython === undefined) {\n",
                                "                        return\n",
                                "                    }\n",
                                '                    var msg = "WARNING: it looks like you might have loaded " +\n',
                                '                        "jupyter_reorder_python_imports in a non-lab notebook with " +\n',
                                '                        "`is_lab=True`. Please double check, and if " +\n',
                                '                        "loading with `%load_ext` please review the README!"\n',
                                "                    console.log(msg)\n",
                                "                    alert(msg)\n",
                                "                })()\n",
                                "                </script>\n",
                                "                ",
                            ],
                            "text/plain": ["<IPython.core.display.HTML object>"],
                        },
                        "metadata": {},
                        "output_type": "display_data",
                    }
                ],
                "source": [
                    "%load_ext jupyter_reorder_python_imports\n",
                    "%load_ext jupyter_black",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": 5,
                "metadata": {},
                "outputs": [],
                "source": ["import re\n", "import datetime"],
            },
            {
                "cell_type": "code",
                "execution_count": 10,
                "metadata": {},
                "outputs": [
                    {
                        "data": {"text/plain": ["1"]},
                        "execution_count": 4,
                        "metadata": {},
                        "output_type": "execute_result",
                    }
                ],
                "source": ["a=1\na"],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "jreorder-1i-52Iue",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.10",
            },
            "orig_nbformat": 4,
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    expected_result = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 100,
                "metadata": {},
                "outputs": [
                    {
                        "data": {
                            "text/html": [
                                "\n",
                                '                <script type="application/javascript" id="jupyter_reorder_python_imports">\n',
                                "                (function() {\n",
                                "                    if (window.IPython === undefined) {\n",
                                "                        return\n",
                                "                    }\n",
                                '                    var msg = "WARNING: it looks like you might have loaded " +\n',
                                '                        "jupyter_reorder_python_imports in a non-lab notebook with " +\n',
                                '                        "`is_lab=True`. Please double check, and if " +\n',
                                '                        "loading with `%load_ext` please review the README!"\n',
                                "                    console.log(msg)\n",
                                "                    alert(msg)\n",
                                "                })()\n",
                                "                </script>\n",
                                "                ",
                            ],
                            "text/plain": ["<IPython.core.display.HTML object>"],
                        },
                        "metadata": {},
                        "output_type": "display_data",
                    }
                ],
                "source": [
                    "%load_ext jupyter_reorder_python_imports\n",
                    "%load_ext jupyter_black",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": 100,
                "metadata": {},
                "outputs": [],
                "source": ["import re\n", "import datetime"],
            },
            {
                "cell_type": "code",
                "execution_count": 100,
                "metadata": {},
                "outputs": [
                    {
                        "data": {"text/plain": ["1"]},
                        "execution_count": 4,
                        "metadata": {},
                        "output_type": "execute_result",
                    }
                ],
                "source": ["a=1\na"],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "jreorder-1i-52Iue",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.10",
            },
            "orig_nbformat": 4,
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    file = tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False)
    with open(file.name, "w") as f:
        json.dump(data, f)
    run(
        [Path(file.name)],
        execution_count=100,
        remove_outputs=False,
        format=False,
        reorder_imports=False,
    )
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result


def test_pyroject() -> None:
    """Test run() with pyproject file"""

    data = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [
                    {
                        "data": {
                            "text/html": [
                                "\n",
                                '                <script type="application/javascript" id="jupyter_reorder_python_imports">\n',
                                "                (function() {\n",
                                "                    if (window.IPython === undefined) {\n",
                                "                        return\n",
                                "                    }\n",
                                '                    var msg = "WARNING: it looks like you might have loaded " +\n',
                                '                        "jupyter_reorder_python_imports in a non-lab notebook with " +\n',
                                '                        "`is_lab=True`. Please double check, and if " +\n',
                                '                        "loading with `%load_ext` please review the README!"\n',
                                "                    console.log(msg)\n",
                                "                    alert(msg)\n",
                                "                })()\n",
                                "                </script>\n",
                                "                ",
                            ],
                            "text/plain": ["<IPython.core.display.HTML object>"],
                        },
                        "metadata": {},
                        "output_type": "display_data",
                    }
                ],
                "source": [
                    "%load_ext jupyter_reorder_python_imports\n",
                    "%load_ext jupyter_black",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": 5,
                "metadata": {},
                "outputs": [],
                "source": ["import re\n", "import datetime"],
            },
            {
                "cell_type": "code",
                "execution_count": 10,
                "metadata": {},
                "outputs": [
                    {
                        "data": {"text/plain": ["1"]},
                        "execution_count": 4,
                        "metadata": {},
                        "output_type": "execute_result",
                    }
                ],
                "source": ["a=1\na"],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "jreorder-1i-52Iue",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.10",
            },
            "orig_nbformat": 4,
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    expected_result = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": "null",
                "metadata": {},
                "outputs": [],
                "source": [
                    "%load_ext jupyter_reorder_python_imports\n",
                    "%load_ext jupyter_black",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": "null",
                "metadata": {},
                "outputs": [],
                "source": ["import datetime\n", "import re"],
            },
            {
                "cell_type": "code",
                "execution_count": "null",
                "metadata": {},
                "outputs": [],
                "source": ["a = 1\n", "a"],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "jreorder-1i-52Iue",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.10",
            },
            "orig_nbformat": 4,
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }

    nb_file = Path("test.ipynb")
    with open(nb_file, "w") as f:
        json.dump(data, f)
    nb_file_exclude = Path("test_exclude.ipynb")
    with open(nb_file_exclude, "w") as f:
        json.dump(data, f)

    args_execution_count = 1000
    args_remove_outputs = False
    args_format = False
    args_reorder_imports = False
    args_files_or_dirs = ["."]
    args_indent_level = 10
    args_exclude_files_or_dir: List[str] = []
    args_ignore_pyproject = False

    (
        project_files_or_dirs,
        project_execution_count,
        project_remove_outputs,
        project_format,
        project_reorder_imports,
        project_indent_level,
        project_exclude_files_or_dir,
    ) = parse_pyproject()
    project_exclude_files_or_dir = [str(nb_file_exclude)]

    (
        files_or_dirs,
        execution_count,
        remove_outputs,
        format,
        reorder_imports,
        indent_level,
        exclude_files_or_dirs,
    ) = process_inputs(
        args_files_or_dirs,
        args_execution_count,
        args_remove_outputs,
        args_format,
        args_reorder_imports,
        args_indent_level,
        args_exclude_files_or_dir,
        args_ignore_pyproject,
        project_files_or_dirs,
        project_execution_count,
        project_remove_outputs,
        project_format,
        project_reorder_imports,
        project_indent_level,
        project_exclude_files_or_dir,
    )

    files = get_lab_files(files_or_dirs)
    exclude_files = get_lab_files(exclude_files_or_dirs)

    run(
        files,
        execution_count,
        remove_outputs,
        format,
        reorder_imports,
        indent_level,
        exclude_files,
    )
    with open(nb_file) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result
    os.unlink(nb_file)
    with open(nb_file_exclude) as f:
        excluded_data = json.load(f)
    assert excluded_data == data
    os.unlink(nb_file_exclude)
