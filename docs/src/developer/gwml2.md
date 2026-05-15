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

---

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

---

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

## Data Models

### Well

The central model. `Well` inherits from `GeneralInformation` and `CreationMetadata` and
holds the core attributes of a groundwater monitoring point:

- Location (PostGIS `Point`), elevation, and status
- Feature type (well, spring, etc.)
- Organisation and ownership
- Links to all related sub-models below

### Measurement Types

Three time-series measurement models, all extending the base `Measurement` class:

| Model | Description |
|-------|-------------|
| `WellLevelMeasurement` | Water level readings over time |
| `WellQualityMeasurement` | Water quality parameter readings |
| `WellYieldMeasurement` | Well yield / discharge readings |

Each measurement stores a timestamp, parameter, value with unit, and QC status.

### Well Detail Models

| Model file | Covers |
|------------|--------|
| `general_information.py` | Name, location, elevation, feature type |
| `hydrogeology.py` | Aquifer type, porosity, hydraulic conductivity |
| `drilling.py` | Drilling method, depth, date |
| `construction.py` | Casing, screen, pump details |
| `management.py` | Owner, operator, purpose, license |
| `geology.py` | Stratigraphic log and lithology |
| `document.py` | Documents attached to a well |
| `reference_elevation.py` | Reference elevation definitions |

### Supporting Models

| Model file | Covers |
|------------|--------|
| `term.py` | Controlled vocabulary terms (feature type, status, etc.) |
| `term_measurement_parameter.py` | Measurement parameter definitions and units |
| `well_management/organisation.py` | Organisation (data owner/operator) |
| `well_management/user.py` | User-organisation relationship |
| `metadata/` | Creation and license metadata mixins |

### Infrastructure Models

| Model file | Covers |
|------------|--------|
| `well_materialized_view.py` | `mv_well` PostgreSQL materialized view — refreshed after harvests for fast map queries |
| `well_quality_control.py` | QC state machine per well |
| `well_cache_indicator.py` | Tracks which wells have generated download cache files |
| `download_request.py` | Tracks async download jobs and their output files |
| `upload_session.py` | Tracks batch upload sessions and validation results |

---

## Responsibilities

### Well Forms

Views and forms for creating, editing, and viewing all well sections. Organised by section
in `views/form_group/`:

- `general_information.py` — basic well info
- `hydrogeology.py` — aquifer and hydraulic properties
- `geology.py` — stratigraphic log
- `drilling.py` — drilling details
- `construction.py` — casing and screen
- `management.py` — ownership and purpose
- `level_measurement.py` / `quality_measurement.py` / `yield_measurement.py` — measurements
- `well_metadata.py` — metadata editing

### Well Download

Export of well data and measurements in multiple formats (CSV, Excel, etc.).
Downloads are backed by a **cache layer** — on first request the data is generated and stored,
subsequent requests serve the cached file.

Cache is managed by Celery tasks in `tasks/data_file_cache/`:

- `wells_cache.py` — per-well general/section cache files
- `organisation_cache.py` — per-organisation aggregate cache
- `country_recache.py` — per-country aggregate cache
- `clean_cache.py` — removes stale cache files

Cache can be regenerated manually via management commands (see below).

### Batch Upload

Import of multiple wells and measurements from spreadsheet files (XLS/XLSX/ODS).
The upload pipeline (`tasks/uploader/`) validates each row and maps it to the GWML2 schema:

- `general_information.py` — well metadata
- `hydrogeology.py` — hydrogeological attributes
- `monitoring_data.py` — measurement time-series
- `drilling_and_construction.py` — drilling details
- `management_data.py` — ownership data

An `UploadSession` model tracks progress, errors, and the final report.

### Well Quality Control

A `WellQualityControl` model and associated Celery task (`tasks/well_quality_control.py`)
run automated checks against well records and flag anomalies. QC status is stored per well
and updated after each harvest or manual edit.

### Harvester System

Pluggable connectors that automatically pull well data from 15 third-party national APIs.
See the [Harvester documentation](../harvester/index.md) for the full list and configuration.

---

## Management Commands

| Command | Description |
|---------|-------------|
| `generate_data_wells_cache` | Regenerate download cache for wells |
| `generate_well_measurement_cache` | Regenerate measurement graph cache |
| `generate_data_countries_cache` | Regenerate country-level download cache |
| `generate_data_organisations_cache` | Regenerate organisation-level download cache |
| `generate_well_quality_control` | Run QC checks across wells |
| `generate_well_metadata` | Rebuild well metadata (count, last measurement date) |
| `generate_well_cache_indicator` | Rebuild cache indicator flags |
| `refresh_materialized_views` | Refresh `mv_well` PostgreSQL materialized view |
| `run_harvesters` | Trigger all active harvesters |
| `assign_country_to_wells` | Fill missing country FK on wells by spatial lookup |
| `update_measurement_type` | Update measurement type classifications |
| `update_number_of_measurements_well` | Recalculate measurement counts on wells |
| `update_fixtures` | Reload all initial data fixtures |
| `clean_download_file` | Remove orphaned download cache files |

---

## Directory Structure

```
gwml2/
├── models/
├── harvesters/                    # Third-party data connectors (15 sources)
├── views/
├── tasks/
├── forms/                         # Django forms
├── api/                           # DRF viewsets
├── serializer/                    # DRF serializers
├── management/commands/           # Management commands (see above)
├── templates/                     # HTML templates
└── migrations/                    # Database migrations
```