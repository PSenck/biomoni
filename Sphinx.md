Create a Sphinx documentation

1. cd to desired directory
2. activate conda:
`conda activae base`
3. install sphinx and check for version:
`pip install -U sphinx`
`sphinx-build --version`
4. optionally install rtd_theme (for different looks):
`pip install sphinx_rtd_theme`
6. Create folder named "Docs"
7. cd to Docs/
8. start sphinx:
	`sphinx-quickstart`
Select correct Settings:
selected root path: `.`
seperate source directories? Enter (n)
Project name: biomoni
Author name: Paul Senck
Project Release: 1.01
select language (en)

open config.py in Docs
remove the comments from:

	import os
	import sys
	sys.path.insert(0, os.path.abspath('.'))

change the last line to navigate to the path where your .py files are present:

`sys.path.insert(0, os.path.abspath('YourPath'))`

write in extensions:
`extensions = ["sphinx.ext.autodoc"]`
optionally change theme
`html_theme = "sphinx_rtd_theme"`

Start documentation with :
`sphinx-apidoc -o InputPath CodePath`
`sphinx-apidoc -o . /biomoni`

open index.rst
add "modules" to toctree:


	.. toctree::
	   :maxdepth: 2
	   :caption: Contents:
	   
	   modules

Make html files:
`make html`

    