.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: test
test:
	pytest --cov=./ --cov-config=.coveragerc

.PHONY: lint
lint:
	ruff --format=github --select=E9,F63,F7,F82 --target-version=py37 .
	ruff --format=github --target-version=py37 .

.PHONY: all
all: install test lint