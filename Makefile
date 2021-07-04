PACKAGE = units 
VRNPATN = '__version__ = "([^"]+)"'
VERSION = $(shell sed -nE 's:__version__ = "([^"]+)":\1:p' ./elle/$(PACKAGE)/__init__.py)
# Documentation
DOCDIR = docs
STYDIR = style
TESTDIR = ~/stdy

PDOC = pdoc --template-dir $(STYDIR) -o $(DOCDIR)

FORCE: 

json: FORCE
	rm json/*
	python etc/build_json.py elle/units/defs.yml json/

install:
	python3 setup.py install
	#pip install -e .



publish:
	python setup.py clean --all sdist
	twine upload --skip-existing dist/*
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags

.PHONY: api

