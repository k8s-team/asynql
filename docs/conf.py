import os
import sys

sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

def _get_project_meta():
    import tomlkit  # noqa: Z435

    with open('../pyproject.toml') as pyproject:
        file_contents = pyproject.read()

    return tomlkit.parse(file_contents)['tool']['poetry']


pkg_meta = _get_project_meta()
project = pkg_meta['name']
copyright = '2019, k8s-team'  # noqa: A001
author = 'k8s-team'

# The short X.Y version
version = pkg_meta['version']
# The full version, including alpha/beta/rc tags
release = version

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',

    # Used to include .md files:
    'm2r',

    # Used to insert typehints into the final docs:
    'sphinx_autodoc_typehints',

    # Used to build graphs:
    'sphinxcontrib.mermaid',
]

autoclass_content = 'class'
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': '',
    'undoc-members': 'code,error_template',
    'exclude-members': '__dict__,__weakref__',
    'show-inheritance': True,
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
add_module_names = False

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_typlog_theme'
html_theme_options = {
    'logo_name': 'asynql',
    'description': (
        'AsyncIO GraphQL client'
    ),
    'github_user': 'k8s-team',
    'github_repo': 'asynql',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
html_sidebars = {
    '**': [
        'logo.html',
        'globaltoc.html',
        'github.html',
        'searchbox.html',
        'moreinfo.html',
    ],
}

# -- Extension configuration -------------------------------------------------

napoleon_numpy_docstring = False

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
