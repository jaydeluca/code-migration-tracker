.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: test
test:
	pytest --cov=./ --cov-config=.coveragerc

.PHONY: lint
lint:
	ruff check

.PHONY: update-examples
update-example:
	pip3 install -r requirements.txt
	python3 main.py -r "open-telemetry/opentelemetry-java-instrumentation" -l "java,groovy" -s "2022-11-15" -i 14 -o "./media/example_output.png"
	python3 main.py -r "open-telemetry/opentelemetry-java-instrumentation" -l "groovy" -s "2022-11-15" -i 14 -o "./media/example_output2.png"
	python3 count_by_instrumentation.py -r "open-telemetry/opentelemetry-java-instrumentation" -l "groovy" -o "./media/example_pie_output.png"

.PHONY: all
all: install test lint