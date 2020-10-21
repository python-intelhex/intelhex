PYTHON := python

define HELP=
Available targets:
 clean   - clean build directory
 test    - run unittest
 epydoc  - run epydoc to create API documentation '(python 2)'
 wininst - Windows installer for Python
 docs    - build docs with ReST and Sphinx
 wheel   - build python wheel binary archive

endef

export HELP
all:
	@echo "$$HELP"

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
	rst2html5.py docs/manual.txt docs/manual.html
	make -C docs/manual html

wheel:
	$(PYTHON) -m pip wheel -w dist .
