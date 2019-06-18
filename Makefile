.PHONY: docs clean lint test mypy flake8 doc8 check safety-check \
		check-for-pull-request

check-for-pull-request: clean
	@echo "check for pull request"
	@$(MAKE) lint
	@$(MAKE) test
	@$(MAKE) check
	@$(MAKE) safety-check

mypy:
	@echo mypy check
	@poetry run mypy asynql tests/**/*.py

flake8:
	@echo flake8 check
	@poetry run flake8 asynql tests docs

doc8:
	@echo doc8 check
	@poetry run doc8 -q docs

lint: mypy flake8 doc8

check:
	@echo "check requirements"
	@poetry check
	@poetry run pip check

safety-check:
	@echo "safety check"
	@poetry run safety check --bare --full-report

test:
	@echo "test"
	@PYTHONPATH=. poetry run pytest

docs: clean
	@echo "clean docs"
	@sphinx-apidoc -o docs/source/sources asynql
	@$(MAKE) -C docs html

clean:
	@echo "clean all"
	rm -rf docs/source/sources
	$(MAKE) -C docs clean
	rm -rf tests-output
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf .pytest_cache
