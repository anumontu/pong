help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install: ## Install requirements from pip
	pip3 install pipenv==2022.1.8
	pipenv install --dev

activate: ## Activate virtual environment
	pipenv shell

pre-commit-install: ## Adds the pre commit hook
	pre-commit install

run_server: ## Run the server
	python pong/server.py

run:
	python pong/client.py
