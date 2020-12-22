requirements.txt: requirements.in
	pip-compile -o $@ $<

.PHONY: upgrade
upgrade:
	pip-compile -U requirements.in

.PHONY: upload
upload:
	rsync -av * pi@plants:mycelium
	ssh pi@plants sudo mycelium/install.sh