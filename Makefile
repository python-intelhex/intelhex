all:
	@echo Available targets:
	@echo  clean - clean build directory
	@echo  test - run unittest
	@echo  epydoc - run epydoc to create API documentation
	@echo  wininst - Windows installer for Python
	@echo  docs - build docs with ReST and Sphinx

.PHONY: clean test epydoc wininst docs

clean:
	python setup.py clean -a

test:
	python setup.py test -q

epydoc:
	epydoc.py -o api -v intelhex

wininst:
	python setup.py bdist_wininst -d.

docs:
	rst2html.py docs/manual.txt docs/manual.html
	make -C docs/manual html
