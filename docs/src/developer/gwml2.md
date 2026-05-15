---
title: gwml2 App
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# `gwml2` — Well and Monitoring Database

Source: [github.com/kartoza/IGRAC-WellAndMonitoringDatabase](https://github.com/kartoza/IGRAC-WellAndMonitoringDatabase)

`gwml2` is a dedicated Django app and Git submodule that handles **all well and monitoring data**
in GGIS. It is the core data layer of the platform — everything related to groundwater wells lives
here, not in GeoNode or the `igrac` app.

The app follows the **GWML2 (Groundwater Markup Language 2)** schema, an OGC standard for
representing groundwater data.

## Separate Database

`gwml2` stores all its data in a **dedicated PostgreSQL/PostGIS database**, separate from the
main GeoNode database. This keeps well data isolated and independently scalable.

The databases are configured via environment variables in `deployment/.env`:

| Variable | Default database | Purpose |
|----------|-----------------|---------|
| `DATABASE_URL` | `geonode` | Main GeoNode application database |
| `GEODATABASE_URL` | `geonode_data` | GeoNode geodata database |
| `GROUNDWATER_DATABASE_URL` | `groundwater` | gwml2 well data database |

In Django settings (`core/settings/base.py`), the `GROUNDWATER_DATABASE_URL` env var is read
and registered as the `gwml2` database alias:

```python
GWML2_DATABASE_CONFIG = 'gwml2'
DATABASES[GWML2_DATABASE_CONFIG] = gwml2_database_conf
```

All `gwml2` models are routed to this alias via a Django database router, so migrations and
queries for well data always hit the `groundwater` database, never `geonode`.

## How Well Data is Served

All well data stored in `gwml2` is served to the map through **GeoNode layers**, using the
**PostgreSQL/PostGIS database as the data store directly** (not via file-based uploads).

GeoServer connects to the same PostGIS database that Django uses, with each layer pointing to
a view or table in the `gwml2` schema. This means:

- Any change to well data is immediately reflected in the map layer without re-publishing.
- GeoNode manages layer metadata, permissions, and styling on top of the live database view.
- There is no intermediate file format (e.g. Shapefile) — the database is the single source
  of truth for both the application and the map.

---

## Responsibilities

### Well and Measurement Database

Data models covering the full lifecycle of a groundwater well:

- Well general information (location, elevation, status)
- Hydrogeology (aquifer type, porosity, hydraulic conductivity)
- Drilling and construction details
- Management information (owner, operator, purpose)
- Measurements: water level, water quality, and well yield, each stored as time-series records

### Harvester System

Pluggable connectors that automatically pull well data from third-party national APIs.
Each harvester is a self-contained module that maps the source data to the GWML2 schema.

Currently supported sources:

- **SGU** (Sweden) — [sgu.se](https://www.sgu.se/)
- **Hubeau** (France) — [hubeau.eaufrance.fr](https://hubeau.eaufrance.fr/api/v1/)

See the [Harvester documentation](../harvester/index.md) for configuration details.

### Well Forms

Django forms and views for creating, viewing, and editing well records and their associated
measurements. Forms cover all sections: general information, hydrogeology, management,
drilling and construction, and each measurement type.

### Well Download

Export of well data and measurements in multiple formats (CSV, Excel, etc.).
Downloads are backed by a **cache layer** — on first request the data is generated and stored,
subsequent requests serve the cached file. Cache can be regenerated via the
`generate_data_wells_cache` and `generate_well_measurement_cache` management commands.

### Batch Upload

Import of multiple wells and measurements from spreadsheet files (XLS/XLSX).
The upload pipeline validates each row against the GWML2 schema before persisting.

### Well Quality Control

Tools for flagging, reviewing, and correcting measurement data. QC status can be set per
measurement record, allowing data managers to mark readings as approved, suspect, or rejected.

---

## Directory Structure

```
gwml2/
├── models/
├── harvesters/                  # Third-party data connectors
├── api/                         # DRF viewsets for well data
├── forms/                       # Well and measurement forms
├── views/                       # Page and API views
├── management/                  # Management commands
├── serializer/                  # DRF serializers
├── tasks/                       # Celery async tasks
├── templates/                   # HTML templates
└── migrations/                  # Database migrations
```