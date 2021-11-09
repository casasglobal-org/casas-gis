.PHONY: setup
setup:
	poetry run install

.PHONY: lint
lint:
	poetry run flake8 casas_gis

.PHONY: test
test:
	poetry run pytest

.PHONY: coverage
cov:
	poetry run pytest --cov=casas_gis --cov-report term-missing
