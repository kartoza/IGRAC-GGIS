---
title: Germany — Lower Saxony
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Germany — Lower Saxony

- **Source:** NLWKN (Niedersächsischer Landesbetrieb für Wasserwirtschaft, Küsten- und Naturschutz)
- **API:** `https://bis.azure-api.net/GrundwasserstandonlinePublic/REST/`
- **Class:** `gwml2.harvesters.harvester.lower_saxony.level.LowerSaxonyHarvester`

## Data Collected

- Water level measurements

## Notes

Requires an API key configured as a `HarvesterAttribute` with the name `api-key`.
Stations are fetched from the `/stammdaten/stationen/allegrundwasserstationen` endpoint.
Measurements are fetched daily using the `/tage/` endpoint.
