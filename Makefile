VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(PYTHON) -m pip

.PHONY: install install-dev run lint format test clean

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install-dev: install
	$(PIP) install -r requirements-dev.txt

run:
	$(VENV)/bin/streamlit run src/mealplan/app.py

lint:
	$(VENV)/bin/ruff check src tests

format:
	$(VENV)/bin/black src tests

test:
	$(VENV)/bin/pytest -q

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache __pycache__ src/__pycache__ tests/__pycache__
