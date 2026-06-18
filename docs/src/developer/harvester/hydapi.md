---
title: Norway — HydAPI / NVE
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Norway — HydAPI / NVE

- **Source:** NVE (Norwegian Water Resources and Energy Directorate) — HydAPI
- **API:** `https://hydapi.nve.no/api/v1/`
- **Class:** `gwml2.harvesters.harvester.hydapi.Hydapi`

## Data Collected

- Water level measurements

## Notes

Stations are fetched from `/Stations`. Measurements are retrieved from `/Observations`
with time-range parameters. Measurement parameters and units are mapped via the
`HarvesterParameterMap` configuration.

See also [Miljødirektoratet](./miljodirektoratet.md) for the separate harvester that
collects water quality data for Norway.