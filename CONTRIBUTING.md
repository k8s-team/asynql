# Contributor's guide

## Dependencies

- [`pyenv`](https://github.com/pyenv/pyenv) - python versions management
- [`poetry`](https://github.com/sdispater/poetry) - dependency management

To install run `poetry install`.

To activate your `virtualenv` run `poetry shell`.

## Tests

- [`pytest`](https://github.com/pytest-dev/pytest/)
- [`pytest-html`](https://github.com/pytest-dev/pytest-html)

Run `pytest`.

## Linters

- [`flake8`](https://github.com/PyCQA/flake8)

Run `flake8 asynql tests docs`.

## Type checks

- [`mypy`](https://github.com/python/mypy)

Run `mypy asynql`.

## Documentation checks

- [`doc8`](https://github.com/openstack/doc8)

Run `doc8`.

## Safety checks

- [`safety`](https://github.com/pyupio/safety)

Run `safety`.

### Before submitting

Before submitting your code please do the following steps:

1. Run `pytest` to make sure everything was working before
2. Add any changes you want
3. Add tests for the new changes
4. Edit documentation if you have changed something significant
5. Update `CHANGELOG.md` with a quick summary of your changes
6. Run `pytest` again to make sure it is still working
7. Run `mypy` to ensure that types are correct
8. Run `flake8` to ensure that style is correct
9. Run `doc8` to ensure that docs are correct
10. Run `safety` to ensure that there are no insecure dependencies
