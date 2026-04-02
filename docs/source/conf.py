import os
import sys

# Le dice a Sphinx dónde está tu código
sys.path.insert(0, os.path.abspath('../../src'))

project = 'Balthu'
author = 'Alejo'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',        # Lee docstrings automáticamente
    'sphinx.ext.napoleon',       # Soporta estilo Google/NumPy en docstrings
    'sphinx.ext.viewcode',       # Agrega links al código fuente
    'sphinx.ext.intersphinx',    # Links a docs de Python, etc.
    'sphinx_autodoc_typehints',  # Convierte type hints en docs
]

# Autodoc: orden de documentación
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'undoc-members': False,  # No documenta cosas sin docstring
    'show-inheritance': True,
}

# Napoleon: estilo de docstrings
napoleon_google_docstyle = True
napoleon_numpy_docstyle = False

html_theme = 'furo'
html_title = 'Mi Agente — Documentación'