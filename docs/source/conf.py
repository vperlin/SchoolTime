# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
import os.path

project = 'SchoolTime'
copyright = '2024, Vladislav Perlin'
author = 'Vladislav Perlin'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

autodoc_default_options = {
    'exclude-members': 'staticMetaObject'
}

latex_engine = 'xelatex'
latex_toplevel_sectioning = 'part'
latex_elements = {
    'fontpkg': r'''
        \setmainfont{FreeSans}
        \setsansfont{FreeSans}
        \setmonofont{FreeMono}
    '''
}

sys.path.insert(0, os.path.abspath('../../src'))

