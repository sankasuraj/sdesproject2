all:
	cd kriging && python curve_fitting_tool.py
test:
	cd tests && python test.py