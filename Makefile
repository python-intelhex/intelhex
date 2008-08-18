all:
	@echo Available targets:
	@echo  clean - clean build directory
	@echo  test - run unittest

clean:
	python setup.py clean -a

test:
	python setup.py test -q
