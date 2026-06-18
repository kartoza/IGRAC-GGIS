---
title: Igrac API and istSOS
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# `igrac_api` and istSOS

GGIS exposes sensor observation data through the **OGC SOS 1.0.0** standard. This is implemented
as a two-layer stack: the `igrac_api` Django app acts as an authenticated gateway, and
**istSOS 2** (running as a separate container) handles the actual SOS protocol.

---

## istSOS 2 (submodule)

Source: [github.com/meomancer/istsos2 — branch igrac](https://github.com/meomancer/istsos2/tree/igrac)

istSOS is an open-source Python implementation of the OGC Sensor Observation Service.
GGIS uses a fork pinned to the `igrac` branch that contains IGRAC-specific patches.

istSOS runs as its own Docker container (`istsos` service) with pre-configured service
definitions located in `deployment/istsos/services/`. It is not exposed directly to the
public — all traffic is routed through `igrac_api`.

### Supported SOS operations

| Operation | Description |
|-----------|-------------|
| `GetCapabilities` | Returns service metadata and available offerings |
| `DescribeSensor` | Returns SensorML description for a given procedure |
| `GetObservation` | Returns time-series measurements for a procedure |
| `InsertObservation` | Inserts new observation records |

---

## `igrac_api` Django App

`igrac_api` is the Django app that sits in front of istSOS. Its responsibilities:

- **Authentication** — validates the `api-key` query parameter on every SOS request before
  forwarding to istSOS. Unauthenticated requests are rejected.
- **Request proxying** — forwards valid SOS requests to the istSOS container and returns the
  XML response unchanged.
- **Download API** — additional REST endpoints for bulk data downloads that do not go through
  istSOS (these return data directly from the `gwml2` database).
- **Celery tasks** — background jobs for generating download files asynchronously.

### Example API calls

**GetCapabilities**
```
GET /istsos?service=SOS&request=GetCapabilities&api-key=<api-key>
```

**DescribeSensor**
```
GET /istsos?service=SOS&version=1.0.0&request=DescribeSensor
    &procedure=<procedure-id>
    &outputFormat=text/xml;subtype="sensorML/1.0.1"
    &api-key=<api-key>
```

---

## Directory Structure

```
igrac_api/
├── api/          # DRF viewsets — SOS proxy and download endpoints
├── serializer/   # DRF serializers
├── tasks/        # Celery tasks (async download generation)
├── forms/        # API key and filter forms
├── models/       # API key model
├── migrations/   # Database migrations
└── urls.py       # URL routing
```

```
deployment/istsos/
├── Dockerfile    # istSOS container image
└── services/     # Pre-configured istSOS service definitions
```
