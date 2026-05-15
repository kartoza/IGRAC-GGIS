---
title: EPA Hydronet (Ireland)
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# EPA Hydronet — Ireland

- **Source:** Environmental Protection Agency (EPA) Ireland — Hydronet
- **API:** `https://epawebapp.epa.ie/Hydronet/output/`
- **Class:** `gwml2.harvesters.harvester.epawebapp.Epawebapp`

## Data Collected

- Water level measurements

## Notes

Data is returned as ZIP files containing CSV. The harvester downloads, extracts, and
parses the CSV content for each station.