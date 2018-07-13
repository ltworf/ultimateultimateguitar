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

deb-pkg: dist
	mv ultimateultimateguitar_`head -1 CHANGELOG`.orig.tar.gz* /tmp
	cd /tmp; tar -xf ultimateultimateguitar*.orig.tar.gz
	cp -r debian /tmp/ultimateultimateguitar/
	cd /tmp/ultimateultimateguitar/; dpkg-buildpackage
	install -d deb-pkg
	mv /tmp/ultimateultimateguitar_* deb-pkg
	$(RM) -r /tmp/ultimateultimateguitar

.PHONY: clean
clean:
	$(RM) -r deb-pkg
