.PHONY: clean fmt check install test


clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	find . -name "*pycache*" | xargs rm -rf

fmt:
	poetry run black argdcls tests
	poetry run blackdoc argdcls tests
	poetry run isort argdcls tests

check:
	poetry run black argdcls tests --check --diff
	poetry run blackdoc argdcls tests --check
	poetry run flake8 --config pyproject.toml --ignore E203,E501,W503 argdcls tests
	poetry run mypy --config pyproject.toml argdcls tests
	poetry run isort argdcls tests --check --diff

install:
	poetry install

test:
	poetry run python3 -m pytest --doctest-modules argdcls tests
