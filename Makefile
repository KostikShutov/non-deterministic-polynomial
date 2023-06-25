##########
# Docker #
##########

.PHONY: d-up
d-up:
	docker-compose up -d

.PHONY: d-down
d-down:
	docker-compose down

.PHONY: d-restart
d-restart:
	docker-compose restart

.PHONY: d-python
d-python:
	docker-compose exec python-ndp bash

###########
# Program #
###########

.PHONY: run
run:
	docker-compose run --rm -w /code python-ndp python main.py
