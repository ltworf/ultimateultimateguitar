.PHONY: mypy
mypy:
	MYPYPATH=stubs mypy --config-file mypy.conf ultimateultimateguitar.py
