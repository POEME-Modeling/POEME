# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import poeme

project = "POEME"
copyright = "2026, POEME Modeling Group"
author = "POEME Modeling Group"
version = poeme.__version__
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

autosummary_generate = True

# suppress_warnings = ["ref.python"]

autodoc_typehints = "signature"
napoleon_use_ivar = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["overrides.css"]


# Auto-run apidoc before every build
import os
import subprocess

subprocess.run(
    [
        "sphinx-apidoc",
        "-f",
        "-e",
        "-o",
        os.path.join(os.path.dirname(__file__), "api"),
        "../src/poeme",  # path to your package, relative to conf.py
    ]
)
