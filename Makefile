PYTHON := python

all:
	@echo Available targets:
	@echo  clean   - clean build directory
	@echo  test    - run unittest
	@echo  epydoc  - run epydoc to create API documentation (python 2)
	@echo  wininst - Windows installer for Python
	@echo  docs    - build docs with ReST and Sphinx
	@echo  wheel   - build python wheel binary archive

.PHONY: clean test epydoc wininst docs

clean:
	$(PYTHON) setup.py clean -a

test:
	$(PYTHON) setup.py test -q

epydoc:
	epydoc.py -o api -v intelhex

wininst:
	$(PYTHON) setup.py bdist_wininst -d.

docs:
	rst2html docs/manual.txt docs/manual.html
	make -C docs/manual html

wheel:
	$(PYTHON) -m pip wheel -w dist .
