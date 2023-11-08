VENV = .venv
PYTHON = $(VENV)/bin/python3 #this is only for unix
PIP = $(VENV)/bin/pip #this is only for unix
export DATA_FOLDER=src/data
export MODEL_FOLDER=src/models

#TODO add a command to download the data and the models using dvc

help:
	@awk 'BEGIN {FS = ":.*##"; printf "\033[35m\033[0m"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$1, 5) } ' $(MAKEFILE_LIST)


##@ Download SRC Files

download_data: ##Download the data files
	$(VENV)/bin/dvc pull src/data --force

download_models: ##Download the models
	$(VENV)/bin/dvc pull src/models --force



build:
	@echo "Hello"


##@ Docker

docker-build: ##builds the docker container
	@docker build -t warehouse-python .

docker-jup: ##creates the jupyter-lab instance
	@docker run -d --name jupyter-lab -v $(CURDIR)/notebooks:/notebooks -p 8888:8888 warehouse-python jupyter lab
	@docker stop jupyter-lab

docker-dash: ##creates the dash app instance
	@docker run -d --name dash-app -v $(CURDIR)/data_app:/data_app -v $(CURDIR)/src:/src -p 8888:8888 warehouse-python python3 /data_app/model_page.py
	@docker stop dash-app

docker-clean: ##removes all instances of the docker containers
	@docker rm dash-app jupyter-lab

##@ Jupyter Lab
launch-jup: ##launches the jupyter lab instance
	@docker start jupyter-lab
	@echo "Go to http://localhost:8888 to access the jupyter notebook"

stop-jup: ##stops the jupyter lab instance
	@docker stop jupyter-lab
	@echo "The jupyter lab instance has been stopped"

##@ Dash App
launch-dash: ##launches the dash app
	@docker start dash-app
	@echo "Go to http://localhost:8888 to access the dash app"

stop-dash: ##stops the dash app
	@docker stop dash-app
	@echo "Dash App has been stopped"

test:
	@echo $(CURDIR)
