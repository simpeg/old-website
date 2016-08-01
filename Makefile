PORT=9080
ADMIN_PORT=8009

.PHONY: build symlinks articles

symlinks:
	cd www/lib && python _symLinks.py

articles:
	python build_article_list.py

build: symlinks articles

run:
	python /usr/local/bin/dev_appserver.py --host=0.0.0.0 --port=$(PORT) --admin_port=$(ADMIN_PORT) www
