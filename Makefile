all:
	@echo Available targets:
	@echo  clean - clean build directory
	@echo  test - run unittest
	@echo  readme - convert Readme.txt to html
	@echo  epydoc - run epydoc to create API documentation

.PHONY: clean test readme epydoc

clean:
	python setup.py clean -a

test:
	python setup.py test -q

readme: README.html

README.html: README.txt
	rst2html.py README.txt README.html

epydoc:
	epydoc.py -v intelhex
