VENV_PATH = ./venv
PYTHON = python3.12
VENV = . $(VENV_PATH)/bin/activate;
VERSION = 0.3.0

.PHONY: clean
clean:
	rm -rf ./*.egg-info
	rm -rf ./.pytest_cache
	rm -rf ./.ruff_cache
	rm -rf ./build
	rm -rf ./dist
	rm -f .version

.PHONY: test
test:
	$(VENV) pytest -o log_cli=true -vv tests/*.py

.phony: e2e
e2e:
	$(VENV) pytest tests/e2e/*.py

.PHONY: build
build:
	echo "$(VERSION)" > .version
	$(VENV) python -m build
	$(VENV) pip install .

.PHONY: lint
lint:
	$(VENV) pylint ./mr_star_ble
	$(VENV) ruff check ./mr_star_ble

.PHONY: qa
qa: lint test

.PHONY: publish
publish:
	$(MAKE) clean
	$(MAKE) build
	git add Makefile
	git commit -m "chore: release $(VERSION)"
	git tag -a $(VERSION) -m "release $(VERSION)"
	$(VENV) python -m twine upload --repository pypi dist/*
	git push && git push --tags

configure:
	rm -rf $(VENV_PATH)
	make $(VENV_PATH)

$(VENV_PATH):
	$(PYTHON) -m venv $(VENV_PATH)
	$(VENV) pip install -r requirements.txt
