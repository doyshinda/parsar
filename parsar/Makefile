
all:
	@python cythonize.py build_ext --inplace
	@cp parsar/cparsar.so .
	@python3 cythonize.py build_ext --inplace
	@cp parsar/cparsar.cpython-34m.so .
	@rm -rf parsar/
