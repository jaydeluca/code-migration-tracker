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

.PHONY: update-examples
update-example:
	pip3 install -r requirements.txt
	python3 main.py -r "open-telemetry/opentelemetry-java-instrumentation" -l "java,groovy" -s "2022-11-15" -i 14 -o "./media/example_output.png"
	python3 main.py -r "open-telemetry/opentelemetry-java-instrumentation" -l "groovy" -s "2022-11-15" -i 14 -o "./media/example_output2.png"


.PHONY: all
all: install test lint