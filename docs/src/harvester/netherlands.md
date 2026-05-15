---
title: BRO (Netherlands)
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# BRO — Netherlands

- **Source:** BRO (Basisregistratie Ondergrond) — Dutch Key Register of the Subsurface
- **API:** `https://api.pdok.nl/bzk/bro-gminsamenhang-karakteristieken/ogc/v1/`
- **Class:** `gwml2.harvesters.harvester.netherland.base.NetherlandHarvester`

## Data Collected

- Well general information
- Water level measurements
- Water quality measurements

## Notes

Stations are paginated via an OGC API Features endpoint. The harvester follows `next` links
until all stations are retrieved.