PROJECT_ID := igrac

SHELL := /bin/bash

# ----------------------------------------------------------------------------
#    P R O D U C T I O N     C O M M A N D S
# ----------------------------------------------------------------------------
default: mapstore-frontend
run: build mapstore-frontend nginx

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) build

mapstore-frontend:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d mapstore-frontend

nginx:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running nginx in production mode"
	@echo "Normally you should use this only for testing"
	@echo "In a production environment you will typically use nginx running"
	@echo "on the host rather if you have a multi-site host."
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d nginx
	@echo "Site should now be available at http://localhost"

up: mapstore-frontend nginx

status:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Show status for all containers"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) ps

kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Killing in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) stop

rm: kill
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Removing production instance!!! "
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) down

# --------------- help --------------------------------

help:
	@echo "* **build** - builds all required containers."
	@echo "* **up** - runs all required containers."
	@echo "* **kill** - kills all running containers. Does not remove them."
	@echo "* **logs** - view the logs of all running containers. Note that you can also view individual logs in the deployment/logs directory."
	@echo "* **nginx** - builds and runs the nginx container."
	@echo "* **permissions** - Update the permissions of shared volumes. Note this will destroy any existing permissions you have in place."
	@echo "* **rm** - remove all containers."
	@echo "* **shell-frontend-mapstore** - open a bash shell in the frontend mapstore (where django runs) container."
