.PHONY: mypy
mypy:
	MYPYPATH=stubs mypy --config-file mypy.conf ultimateultimateguitar.py


.PHONY: install
install:
	# Install command
	install -D ultimateultimateguitar.py $${DESTDIR:-/}/usr/bin/ultimateultimateguitar
	# install extras
	install -m644 -D CHANGELOG $${DESTDIR:-/}/usr/share/doc/ultimateultimateguitar/CHANGELOG

.PHONY: dist
dist:
	cd ..; tar -czvvf ultimateultimateguitar.tar.gz \
		ultimateultimateguitar/CHANGELOG \
		ultimateultimateguitar/LICENSE \
		ultimateultimateguitar/Makefile \
		ultimateultimateguitar/mypy.conf \
		ultimateultimateguitar/README.md \
		ultimateultimateguitar/requirements.txt \
		ultimateultimateguitar/stubs/ \
		ultimateultimateguitar/ultimateultimateguitar.py
	mv ../ultimateultimateguitar.tar.gz ultimateultimateguitar`head -1 CHANGELOG`.orig.tar.gz
	gpg --detach-sign -a *.orig.tar.gz
