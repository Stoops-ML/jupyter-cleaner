import json
import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest
from jupyter_cleaner.jupyter_cleaner import main


def test_defaults() -> None:
    """Default behaviour is to not edit the original notebook"""
    data = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {"collapsed": True},
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
                "source": [],
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
    with mock.patch.object(
        sys, "argv", ["jupyter-cleaner", file.name, "--ignore_pyproject"]
    ):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == data


def test_execution_count() -> None:
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--execution_count",
        "100",
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result


def test_clear_cell_metadata() -> None:
    data = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {"collapsed": True},
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--clear_cell_metadata",
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result


def test_preserve_cell_metadata() -> None:
    data = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {"collapsed": True, "editable": False},
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
                "execution_count": 1,
                "metadata": {"collapsed": True},
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--preserve_cell_metadata",
        "collapsed",
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result


def test_remove_empty_cells() -> None:
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
                "source": [],
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
        "cells": [],
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--remove_empty_cells",
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result


def test_reorder_imports() -> None:
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
                "source": ["import datetime\n", "import re"],
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
                "source": ["a=1\n", "a"],
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--execution_count",
        "-1",
        "--ignore_pyproject",
        "--reorder_imports",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result


def test_format() -> None:
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
                "source": ["import re \n", "import  datetime"],
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--ignore_pyproject",
        "--format",
        "--execution_count",
        "-1",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result


def test_remove_outputs() -> None:
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
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
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
                "outputs": [],
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--remove_outputs",
        "--execution_count",
        "-1",
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result


def test_exclude_files_or_dirs() -> None:
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

    file = tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False)
    with open(file.name, "w") as f:
        json.dump(data, f)
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--exclude_files_or_dirs",
        file.name,
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
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

    input_args = [
        "jupyter-cleaner",
        ".",
        "--execution_count",
        "1000",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()

    with open(nb_file) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result
    os.unlink(nb_file)


def test_end_of_file() -> None:
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
    with mock.patch.object(sys, "argv", ["jupyter-cleaner", file.name]):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == expected_result
    with open(file.name) as f:
        assert f.read()[-1] == "\n"


def test_no_cell_source() -> None:
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
                "source": [],
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--format",
        "--reorder_imports",
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == data


def test_markdown_cell() -> None:
    data = {
        "cells": [
            {
                "attachments": {},
                "cell_type": "markdown",
                "metadata": {},
                "source": ["Markdown text."],
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--format",
        "--reorder_imports",
        "--execution_count",
        "100",
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == data


def test_shell_in_code_cell() -> None:
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
                "source": ["    !dir"],
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
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
    with open(file.name) as f:
        formatted_data = json.load(f)
    assert formatted_data == data


def test_stop_at_fail() -> None:
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
    str_data = json.dumps(data)

    file = tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False)
    with open(file.name, "w") as f:
        f.write(str_data[:-1])
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--execution_count",
        "100",
        "--ignore_pyproject",
    ]
    with mock.patch.object(sys, "argv", input_args), pytest.raises(
        json.decoder.JSONDecodeError
    ):
        main()


def test_ignore_fails() -> None:
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
    str_data = json.dumps(data)

    file = tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False)
    with open(file.name, "w") as f:
        f.write(str_data[:-1])
    input_args = [
        "jupyter-cleaner",
        file.name,
        "--execution_count",
        "100",
        "--ignore_pyproject",
        "--ignore_fails",
    ]
    with mock.patch.object(sys, "argv", input_args):
        main()
