VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MKDOCS := $(VENV)/bin/mkdocs

.PHONY: venv activate install serve build-html build-pdf clean help

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  venv        Create Python virtual environment in ./venv"
	@echo "  activate    Print command to activate the virtual environment"
	@echo "  install     Install Python dependencies into the virtual environment"
	@echo "  serve       Run live-reload dev server at http://localhost:8000"
	@echo "  build-html  Build static HTML site to docs/site/"
	@echo "  build-pdf   Build PDF document"
	@echo "  clean       Remove generated site/ directory"

venv:
	python3 -m venv $(VENV)
	@echo "Virtual environment created. Run 'make activate' to see how to activate it."

activate:
	@echo "Run the following command to activate the virtual environment:"
	@echo ""
	@echo "  source $(VENV)/bin/activate"

install: venv
	$(PIP) install -r requirements.txt

serve: install
	bash create-mkdocs-html-config.sh
	$(MKDOCS) serve

build-html: install
	bash build-docs-html.sh

build-pdf: install
	bash build-docs-pdf.sh

clean:
	rm -rf site/