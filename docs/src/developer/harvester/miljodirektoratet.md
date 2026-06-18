---
title: Norway — Miljødirektoratet
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Norway — Miljødirektoratet

- **Source:** Norwegian Environment Agency (Miljødirektoratet) — Vannmiljø API
- **API:** `https://vannmiljoapi.miljodirektoratet.no/api/`
- **Swagger:** `https://vannmiljoapi.miljodirektoratet.no/swagger/ui/index`
- **Class:** `gwml2.harvesters.harvester.miljodirektoratet.base.MiljodirektoratetHarvester`

## Data Collected

- Water quality measurements

## Notes

Requires an API key configured as a `HarvesterAttribute` with the name `api-key`.
Measurements are retrieved via the `Public/GetRegistrations` endpoint.

See also [Hydapi](./hydapi.md) for the separate NVE harvester that collects water level
data for Norway.