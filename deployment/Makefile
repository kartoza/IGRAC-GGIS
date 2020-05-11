PROJECT_ID := igrac

SHELL := /bin/bash

# ----------------------------------------------------------------------------
#    P R O D U C T I O N     C O M M A N D S
# ----------------------------------------------------------------------------
default: mapstore-frontend
run: build mapstore-frontend nginx mapstore-backend db db-setup

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

mapstore-backend:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d mapstore-backend

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

db:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d db

db-setup:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Initializing DB"
	@echo "------------------------------------------------------------------"
	@docker exec -it $(PROJECT_ID)-mapstore-db su - postgres -c "psql -c \"DROP DATABASE IF EXISTS geostore;\""
	@docker exec -it $(PROJECT_ID)-mapstore-db su - postgres -c "psql < /docker-entrypoint-initdb.d/001_setup_db.sql"
	@docker exec -it $(PROJECT_ID)-mapstore-db su - postgres -c "psql geostore < /docker-entrypoint-initdb.d/002_create_schema_postgres.sql"

db-restore: db-setup
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Adding Rows"
	@echo "------------------------------------------------------------------"
	@docker exec -it $(PROJECT_ID)-mapstore-db su - postgres -c "psql geostore < /docker-entrypoint-initdb.d/003_restore_db.sql"

up: mapstore-frontend nginx mapstore-backend db

shell-backend:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Entering Mapstore Backend Shell"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)-mapstore-backend sh

shell-frontend:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Entering Mapstore Frontend Shell"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)-mapstore-frontend sh

shell-db:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Entering Mapstore DB Shell"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)-mapstore-db sh

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
	@echo "* **shell-frontend** - open a bash shell in the frontend mapstore (where django runs) container."
	@echo "* **shell-backend** - open a bash shell in the backend mapstore (where django runs) container."
