.PHONY: clean format check install uninstall test pypi

venv:
	which python3
	python3 -m venv venv

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	find . -name "*pycache*" | xargs rm -rf

format:
	black argdcls
	blackdoc argdcls
	isort argdcls

check:
	black argdcls --check --diff
	blackdoc argdcls --check
	flake8 --config pyproject.toml --ignore E203,E501,W503 argdcls
	mypy --config pyproject.toml argdcls
	isort argdcls --check --diff

install:
	python3 setup.py install

uninstall:
	python3 -m pip uninstall argdcls -y

test:
	python3 -m pytest --doctest-modules
