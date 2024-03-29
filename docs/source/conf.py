# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

import elfws.version

# -- Project information -----------------------------------------------------

project = u'eda-log-file-warning-suppressor'
copyright = u'2020, Jeremiah C Leary'
author = u'Jeremiah C Leary'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx_rtd_theme']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

html_sidebars = {
    '**': [
        'relations.html',
        'searchbox.html',
        ]
}

source_suffic = '.rst'

master_doc = 'index'

version = str(elfws.version.version)

release = str(elfws.version.version)

language = 'en'

pygments_style = 'sphinx'

html_theme_options = {
  'logo_only': False,
  'display_version': True,
#  'prev_next_bottons_location': 'bottom',
  'style_external_links': False,
  'vcs_pageview_mode': '',
#  'style_nav_header_background': 'white',
  # ToC options
  'collapse_navigation': False,
  'sticky_navigation': True,
  'navigation_depth': 3,
  'includehidden': False,
  'titles_only': False
}

