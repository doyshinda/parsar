.PHONY: local build push pushtest

local: build
	@sudo pip2.7 install -e .

build:
	@python2.7 setup.py sdist

pushtest: build
	@twine upload -r pypitest dist/*

pushprod: build
	@twine upload -r pypi dist/*
