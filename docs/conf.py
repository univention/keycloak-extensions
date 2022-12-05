# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import sys

# sys.path.insert(0, os.path.abspath('.'))

from datetime import date
from sphinx.locale import _


# -- Project information -----------------------------------------------------
def read_version_from_env_var() -> str:
    return os.environ.get("DOC_TARGET_VERSION", "0.0.0")


def read_doc_name_from_env_var() -> str:
    return os.environ.get("DOC_TARGET_NAME", "document-name")


#  These variables are required.
version = read_version_from_env_var()
basename = read_doc_name_from_env_var()

release = version
project = "Keycloak Extensions {}".format(release)
copyright = '{}, Univention GmbH'.format(date.today().year)
author = 'Univention GmbH'
language = 'en'
html_title = project
doc_basename = basename

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_copybutton",
    "sphinxcontrib.spelling",
    "univention_sphinx_extension",
    "sphinx_sitemap",
    "sphinx_last_updated_by_git",
    "sphinxcontrib.inkscapeconverter",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.bibtex",
    "sphinx_inline_tabs",
]

bibtex_bibfiles = ["bibliography.bib"]
bibtex_encoding = "utf-8"
bibtex_default_style = "unsrt"
bibtex_reference_style = "label"

# For more configuration options of Sphinx-copybutton, see the documentation
# https://sphinx-copybutton.readthedocs.io/en/latest/index.html
copybutton_prompt_text = r"\$ "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"
copybutton_here_doc_delimiter = "EOT"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

pdf_doc_base = basename

html_theme = "univention_sphinx_book_theme"

html_context = {
    "pdf_download_filename": f"{basename}.pdf",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: List[str] = []  # value is usally ['_static']

html_last_updated_fmt = "%a, %d. %b %Y at %H:%m (UTC%z)"

numfig = True
suppress_warnings = ["git.too_shallow"]

if "spelling" in sys.argv:
    spelling_lang = "en"
    spelling_show_suggestions = True
    spelling_word_list_filename = ["spelling_wordlist"]

linkcheck_ignore: List[str] = []

root_doc = "index"

rst_epilog = """
.. include:: /links.txt

.. include:: /abbreviations.txt
"""

intersphinx_mapping = {
    "uv-manual": ("https://docs.software-univention.de/manual/5.0/en", None)
}

latex_engine = "lualatex"
latex_show_pagerefs = True
latex_show_urls = "footnote"
latex_documents = [(root_doc, f"{basename}.tex", project, author, "manual", False)]
latex_elements = {
    "papersize": "a4paper",
}

# See Univention Sphinx Extension for its options and information about the
# feedback link.
# https://git.knut.univention.de/univention/documentation/univention_sphinx_extension
univention_feedback = True
univention_doc_basename = basename
