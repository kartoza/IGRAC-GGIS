---
title: Project Structure
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Project Structure

## Built on GeoNode

GGIS is built on top of **GeoNode**, an open-source geospatial content management system.
GeoNode provides the foundational infrastructure: user management, map/layer/document publishing,
GeoServer integration, and the Mapstore2-based map viewer.

IGRAC uses a forked version of GeoNode (`4.4.3.igrac`) that contains IGRAC-specific patches and
customisations. This fork lives at
[github.com/kartoza/geonode — branch 4.4.3.igrac](https://github.com/kartoza/geonode/tree/4.4.3.igrac)
and is included in this repository as a Git submodule.

The `igrac` Django app is itself a GeoNode app — it registers against GeoNode's extension
points and overrides templates, signals, and settings. However it contains a large amount of
GGIS-specific logic that goes well beyond what a typical GeoNode installation provides.

On top of GeoNode, GGIS adds:

- A full **well and monitoring database** (the `gwml2` app, also a submodule).
- **IGRAC-specific UI** customisations, models, admin pages, and REST API endpoints.
- An **istSOS 2** integration for serving sensor observation data (OGC SOS 1.0.0).
- A **Harvester** system for pulling well data from third-party national APIs.

---

## Repository Layout

```
IGRAC-GGIS/
├── deployment/       # Infrastructure: Docker Compose, Nginx, GeoServer, Makefile
├── django_project/   # Django source code (IGRAC apps)
├── docs/             # MkDocs documentation (this site)
├── geonode/          # GeoNode fork (Git submodule)
├── istsos2/          # istSOS 2 fork (Git submodule)
└── playwright/       # End-to-end browser tests
```

---

## `deployment/`

Everything needed to run the stack via Docker Compose.

```
deployment/
├── docker/                              # Build context for the Django image
│   ├── Dockerfile                       # Multi-stage: prod → dev
│   ├── entrypoint.sh                    # Container startup script
│   ├── initialize.py                    # Runs migrations and fixtures on startup
│   ├── REQUIREMENTS.txt                 # Production Python dependencies
│   ├── REQUIREMENTS-DEV.txt             # Extra dev dependencies (e.g. debugpy)
│   └── uwsgi.conf                       # uWSGI configuration for production
├── docker-mapstore/
│   └── Dockerfile                       # Mapstore2 frontend image
├── geoserver/
│   ├── Dockerfile                       # GeoServer image customisation
│   ├── entrypoint.sh                    # GeoServer startup script
│   └── download.properties              # GeoServer download configuration
├── istsos/
│   ├── Dockerfile                       # istSOS container image
│   └── services/                        # Pre-configured istSOS service definitions
├── nginx/
│   ├── sites-enabled/                   # Nginx virtual host configs
│   └── pages/                           # Static error pages served by Nginx
├── backups/                             # Database backup scripts/config
├── volumes/                             # Runtime data (gitignored)
│   ├── statics/                         # Django collected statics and media
│   └── logs/                            # Nginx and app logs
├── docker-compose.yml                   # Base service definitions
├── docker-compose.override.template.yml # Minimal override template
├── docker-compose.override.local.template.yml  # Local dev override template
├── image-index.yml                      # Pinned image versions
└── Makefile                             # Developer shortcut commands
```

---

## `django_project/`

The Django application. IGRAC extends GeoNode by adding its own Django apps here.

```
django_project/
├── core/             # Project-level Django configuration
│   ├── settings/
│   │   ├── base.py   # Shared settings (extends GeoNode settings)
│   │   ├── prod.py   # Production overrides
│   │   ├── dev.py    # Development overrides
│   │   └── test.py   # Test overrides
│   ├── api/          # Core API utilities
│   ├── views/        # Core views (e.g. health check)
│   ├── urls.py       # Root URL configuration
│   └── wsgi.py       # WSGI entry point
├── gwml2/            # Well and monitoring database app (Git submodule)
├── igrac/            # Main IGRAC app — UI, models, admin
├── igrac_api/        # REST/SOS API — proxies requests to istSOS
├── version/          # Version tracking scripts and files
└── manage.py         # Django management entry point
```

Each app is documented in detail on its own page:

- [gwml2 — Well and Monitoring Database](./gwml2.md)
- [igrac — Main GGIS App](./igrac.md)
- [igrac_api and istSOS](./igrac_api_and_istsos.md)

---

## `geonode/` (submodule)

Kartoza's fork of GeoNode, pinned to the `4.4.3.igrac` branch.
Source: [github.com/kartoza/geonode](https://github.com/kartoza/geonode/tree/4.4.3.igrac)

This submodule is mounted into the Docker image at build time (see `deployment/docker/Dockerfile`).
Do not edit files inside this directory directly — changes belong in the upstream fork.

---

## `docs/`

MkDocs documentation project (this site). See [Documentation](./documentation.md) for details
on structure, how to run it locally, and how to add new pages.

---

## `playwright/`

End-to-end browser tests run against a live staging environment.

```
playwright/
└── staging-tests/
    ├── tests/
    │   ├── landingPage.spec.ts
    │   ├── maps.spec.ts
    │   ├── dashboards.spec.ts
    │   ├── documents.spec.ts
    │   ├── geostories.spec.ts
    │   ├── data-map-layers.spec.ts
    │   └── well-and-monitoring-data.spec.ts
    ├── playwright.config.ts
    └── run-tests.sh
```

Tests cover the main user-facing pages: landing page, maps, dashboards, documents,
geostories, data/map layers, and the well and monitoring data portal.