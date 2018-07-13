.PHONY: mypy
mypy:
	MYPYPATH=stubs mypy --config-file mypy.conf ultimateultimateguitar.py


.PHONY: install
install:
	# Install command
	install -D ultimateultimateguitar.py $${DESTDIR:-/}/usr/bin/ultimateultimateguitar
	# install extras
	install -m644 -D CHANGELOG $${DESTDIR:-/}/usr/share/doc/ultimateultimateguitar/CHANGELOG
