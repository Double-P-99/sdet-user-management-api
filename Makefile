PYTHON ?= python
VENV_DIR ?= .venv
ifeq ($(OS),Windows_NT)
	VENV_PYTHON := $(VENV_DIR)\Scripts\python.exe
else
	VENV_PYTHON := $(VENV_DIR)/bin/python
endif
PIP ?= $(VENV_PYTHON) -m pip
PYTEST ?= $(VENV_PYTHON) -m pytest
DOCKER ?= docker
IMAGE ?= ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest
CONTAINER_NAME ?= sdet-user-api
BASE_URL ?= http://localhost:3000
AUTH_TOKEN ?= mysecrettoken
REQUEST_TIMEOUT ?= 10
REQUEST_RETRIES ?= 2

.PHONY: help setup install env up down restart logs test test-dev test-prod test-contract test-unit

help:
	@echo "Available targets:"
	@echo "  make setup         Create virtualenv, install dependencies, and create .env if missing"
	@echo "  make venv          Create the local virtual environment"
	@echo "  make install       Install Python dependencies into the virtual environment"
	@echo "  make env           Create .env from .env.example if missing"
	@echo "  make up            Start the API container"
	@echo "  make down          Stop and remove the API container"
	@echo "  make restart       Restart the API container"
	@echo "  make logs          Show API container logs"
	@echo "  make test-dev      Run tests against the dev environment"
	@echo "  make test-prod     Run tests against the prod environment"
	@echo "  make test          Run tests against the current TEST_ENV or default dev"
	@echo "  make test-contract Run contract-only tests"
	@echo "  make test-unit     Run framework unit tests without the API container"

setup: venv install env

.PHONY: venv

venv:
	$(PYTHON) -m venv $(VENV_DIR)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

env:
	$(PYTHON) -c "from pathlib import Path; src = Path('.env.example'); dst = Path('.env'); dst.write_text(src.read_text()) if src.exists() and not dst.exists() else None"

up:
	$(DOCKER) run -d --name $(CONTAINER_NAME) -p 3000:3000 $(IMAGE)

down:
	-$(DOCKER) rm -f $(CONTAINER_NAME)

restart: down up

logs:
	$(DOCKER) logs -f $(CONTAINER_NAME)

test:
	BASE_URL=$(BASE_URL) AUTH_TOKEN=$(AUTH_TOKEN) REQUEST_TIMEOUT=$(REQUEST_TIMEOUT) REQUEST_RETRIES=$(REQUEST_RETRIES) $(PYTEST) -m "not unit" --html=reports/report.html --self-contained-html --junitxml=reports/results.xml

test-dev:
	TEST_ENV=dev BASE_URL=$(BASE_URL) AUTH_TOKEN=$(AUTH_TOKEN) REQUEST_TIMEOUT=$(REQUEST_TIMEOUT) REQUEST_RETRIES=$(REQUEST_RETRIES) $(PYTEST) -m "not unit" --html=reports/dev-report.html --self-contained-html --junitxml=reports/dev-results.xml

test-prod:
	TEST_ENV=prod BASE_URL=$(BASE_URL) AUTH_TOKEN=$(AUTH_TOKEN) REQUEST_TIMEOUT=$(REQUEST_TIMEOUT) REQUEST_RETRIES=$(REQUEST_RETRIES) $(PYTEST) -m "not unit" --html=reports/prod-report.html --self-contained-html --junitxml=reports/prod-results.xml

test-contract:
	TEST_ENV=dev BASE_URL=$(BASE_URL) AUTH_TOKEN=$(AUTH_TOKEN) REQUEST_TIMEOUT=$(REQUEST_TIMEOUT) REQUEST_RETRIES=$(REQUEST_RETRIES) $(PYTEST) -m contract --html=reports/contract-report.html --self-contained-html --junitxml=reports/contract-results.xml

test-unit:
	TEST_ENV=dev BASE_URL=$(BASE_URL) AUTH_TOKEN=$(AUTH_TOKEN) REQUEST_TIMEOUT=$(REQUEST_TIMEOUT) REQUEST_RETRIES=$(REQUEST_RETRIES) $(PYTEST) -m unit
