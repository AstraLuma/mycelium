requirements.txt: requirements.in
	pip-compile -o $@ $<

.PHONY: upgrade
upgrade:
	pip-compile -U -o requirements.txt requirements.in

.PHONY: upload
upload: requirements.txt
	rm -rf __pycache__
	rsync -av * pi@plants:mycelium
	ssh pi@plants sudo mycelium/install.sh
