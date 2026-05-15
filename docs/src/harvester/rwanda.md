---
title: RWB (Rwanda)
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# RWB — Rwanda

- **Source:** Rwanda Water Board (RWB)
- **API:** `https://www.waterapi.rwb.rw/`
- **Class:** `gwml2.harvesters.harvester.rwanda.base.RwandaHarvester`

## Data Collected

- Well general information
- Water level measurements

## Notes

Stations are fetched via `getLocationData`. Measurements are retrieved via
`getTimeSeriesDescriptionList` and `getTimeSeriesData`.