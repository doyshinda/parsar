.PHONY: local build push

local: build
	@sudo pip2.7 install -e .

build: cythonize
	@python2.7 setup.py sdist

cythonize:
	@make -C parsar/

pushtest: build
	@cp dist/* ../parsar-archive/
	@rm -f dist/*
	@twine upload -r pypitest dist/*
