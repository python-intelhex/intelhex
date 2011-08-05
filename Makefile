PYTHON := python

all:
	@echo Available targets:
	@echo  clean - clean build directory
	@echo  test - run unittest
	@echo  epydoc - run epydoc to create API documentation
	@echo  wininst - Windows installer for Python
	@echo  docs - build docs with ReST and Sphinx
	@echo  2to3 - convert source code using 2to3 converter
	@echo  3to2 - convert sources back after 2to3 (bzr revert)

.PHONY: clean test epydoc wininst docs 2to3 3to2

clean:
	$(PYTHON) setup.py clean -a

test:
	$(PYTHON) setup.py test -q

epydoc:
	epydoc.py -o api -v intelhex

wininst:
	$(PYTHON) setup.py bdist_wininst -d.

docs:
	rst2html.py docs/manual.txt docs/manual.html
	make -C docs/manual html

2to3:
	$(PYTHON) tools/2to3.py --no-diff --write --nobackups intelhex
	python tools/crlf.py intelhex/__init__.py intelhex/bench.py intelhex/test.py
	$(PYTHON) tools/2to3.py --no-diff --write --nobackups scripts
	python tools/crlf.py scripts/bin2hex.py scripts/hex2bin.py scripts/hex2dump.py \
		scripts/hexdiff.py scripts/hexmerge.py

3to2:
	bzr revert --no-backup intelhex scripts 
