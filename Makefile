PYTHON := python

all:
	@echo Available targets:
	@echo  clean   - clean build directory
	@echo  test    - run unittest
	@echo  apidoc  - run epdoc to create API documentation
	@echo  wininst - Windows installer for Python
	@echo  docs    - build docs with ReST and Sphinx
	@echo  wheel   - build python wheel binary archive

.PHONY: clean test epydoc wininst docs

clean:
	$(PYTHON) setup.py clean -a

test:
	$(PYTHON) setup.py test -q

apidoc:
	pdoc -o docs/api --html -f intelhex

wininst:
	$(PYTHON) setup.py bdist_wininst -d.

docs:
	rst2html5.py docs/manual.txt docs/manual.html
	$(MAKE) -C docs/manual html

wheel:
	$(PYTHON) -m pip wheel -w dist .
