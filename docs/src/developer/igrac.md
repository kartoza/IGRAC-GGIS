---
title: igrac App
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# `igrac` — Main GGIS App

The `igrac` app is the primary Django application in GGIS. It is a **GeoNode app** — it
registers against GeoNode's extension points (signals, settings, template overrides) — but it
contains a large amount of GGIS-specific logic that goes well beyond a typical GeoNode app.

Everything that is specific to the IGRAC portal but not related to well data (which lives in
`gwml2`) or the SOS API (which lives in `igrac_api`) is implemented here.

---

## Responsibilities

### Site Preferences

A `SitePreference` singleton model controls portal-wide settings: default map extent,
featured layers, contact details, and other configurable values that site administrators
can change through Django Admin without a code deployment.

### GeoNode UI Customisations

- Override and extend GeoNode templates (map viewer, layer detail, home page, etc.)
- Custom context processors that inject IGRAC-specific data into every page
- Monkey-patches for GeoNode behaviour that cannot be overridden cleanly via settings
- Custom static assets (CSS/JS) layered on top of the GeoNode/Mapstore2 frontend

### Map and Layer Models

- `GroundwaterLayer` — links a GeoNode layer to a groundwater data category, controlling how
  it appears in the thematic map viewers
- `MapSlug` — human-readable URL slugs for maps
- Fixtures for pre-seeding the portal with standard groundwater layer categories

### User Profiles and Registration

- Extended `UserProfile` model with organisation, country, and data-access fields
- Custom registration page and approval workflow on top of GeoNode's default registration

### Management Commands

| Command | Description |
|---------|-------------|
| `import_documents` | Bulk-import documents from a directory into GeoNode |
| `update_map_slug` | Regenerate URL slugs for all maps |
| `clean_style` | Remove orphaned GeoNode layer styles |

---

## Directory Structure

```
igrac/
├── models/
├── admin/                    # Django Admin classes
├── api_views/                # Non-SOS REST views
├── forms/                    # User, profile, and preference forms
├── templates/                # HTML templates (overrides GeoNode templates)
├── static/                   # JS/CSS assets
├── management/
├── migrations/               # Database migrations
├── fixtures/                 # Initial data (layer categories, terms, etc.)
├── locale/                   # i18n translation strings
├── context_processors.py     # Template context injections
├── monkeypatch.py            # GeoNode behaviour overrides
├── signals.py                # Django signal handlers
├── templatetags/             # Custom template tags and filters
└── urls.py                   # URL routing
```