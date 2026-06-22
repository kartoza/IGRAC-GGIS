---
title: Deployment
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Deployment

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)
- `make`

---

## Quick Start

Clone the repository and initialise submodules:

```bash
git clone https://github.com/kartoza/IGRAC-GGIS.git
cd IGRAC-GGIS
git submodule init
git submodule update
```

Copy the override template and configure your local environment:

```bash
cd deployment
cp docker-compose.override.local.template.yml docker-compose.override.yml
```

Start the stack:

```bash
make deploy
```

The site will be available at `http://localhost/`.

---

## Development Mode

To run the development server (with hot-reloading Django via `runserver`):

```bash
make dev
```

Wait for the database to be ready, then run the entrypoint and start the dev server:

```bash
make dev-entrypoint
make dev-runserver
```

Open a shell inside the dev container:

```bash
make dev-shell
```

---

## Docker Services

| Service     | Description                               |
|-------------|-------------------------------------------|
| `django`    | Main Django/GeoNode application (uWSGI)   |
| `dev`       | Django development server (port 8080)     |
| `celery`    | Async task worker                         |
| `db`        | PostgreSQL/PostGIS database               |
| `geoserver` | GeoServer spatial data server             |
| `nginx`     | Reverse proxy (port 80)                   |
| `rabbitmq`  | Message broker for Celery                 |

---

## Common Make Commands

| Command              | Description                               |
|----------------------|-------------------------------------------|
| `make deploy`        | Build images and bring up all containers  |
| `make dev`           | Start the celery and dev containers       |
| `make build`         | Build all Docker images from scratch      |
| `make up`            | Start all containers (no build)           |
| `make kill`          | Stop all running containers               |
| `make rm`            | Stop and remove all containers            |
| `make shell`         | Open a bash shell in the Django container |
| `make dev-shell`     | Open a bash shell in the dev container    |
| `make db-shell`      | Open a PostgreSQL shell                   |
| `make migrate`       | Run Django database migrations            |
| `make collectstatic` | Collect Django static files               |
| `make status`        | Show status of all containers             |
| `make dev-test`      | Run the test suite                        |

---

## Environment Variables

Configuration is managed through a `.env` file in the `deployment/` directory.
Copy the template and fill in the required values before starting the stack:

```bash
cp .env.template .env
```

Key variables include database credentials, GeoServer configuration, and `HTTP_HOST` / `HTTP_PORT`
for the public URL.

---

## Running Tests

```bash
make dev-test
```

This runs `python manage.py test gwml2.tests` inside the dev container.

---

## Management Commands

These Django management commands are available inside the Django or dev container
(`make shell` / `make dev-shell`):

### `generate_data_wells_cache`

Generates download cache for wells.

```
--id              ID of the well to process
--from_id         Start ID for batch processing
--country_code    Filter wells by country
--force           Regenerate cache even if it already exists
--generator       Comma-separated list of sections to generate:
                  general_information, hydrogeology, management,
                  drilling_and_construction, monitor
```

### `generate_data_countries_cache`

Generates download cache for countries.

```
--country_code   Country code to regenerate
```

### `generate_data_organisations_cache`

Generates download cache for organisations.

```
--id        ID of the organisation to process
--from_id   Start ID for batch processing
```

### `update_measurement_type`

Updates the measurement type of wells.

```
--form   Start ID for batch processing
```

### `update_number_of_measurements_well`

Updates the measurement count for wells.

```
--form   Start ID for batch processing
```

---

## Updating Submodules

The project uses two Git submodules: `geonode` and `gwml2`.

To pull the latest changes for both:

```bash
git submodule update --remote
```

To update a specific submodule to a new tag, edit the `GWML2_VERSION` or `GEONODE_VERSION`
build arg in `deployment/docker/Dockerfile`, then rebuild:

```bash
make build
make deploy
```