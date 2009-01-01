all:
	@echo Available targets:
	@echo  clean - clean build directory
	@echo  test - run unittest
	@echo  epydoc - run epydoc to create API documentation
	@echo  wininst - Windows installer for Python

.PHONY: clean test epydoc wininst

clean:
	python setup.py clean -a

test:
	python setup.py test -q

epydoc:
	epydoc.py -o api -v intelhex

wininst:
	python setup.py bdist_wininst -d.
