.PHONY: docs clean lint test mypy flake8

mypy:
	@echo mypy check
	poetry run mypy asynql

flake8:
	@echo flake8 check
	@poetry run flake8 asynql tests docs

lint: mypy flake8

test:
	pytest

docs: clean
	sphinx-apidoc -o docs/source/sources asynql
	$(MAKE) -C docs html

clean:
	rm -rf docs/source/sources
	$(MAKE) -C docs clean
