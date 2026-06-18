---
title: New Zealand — GNS CRI
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# New Zealand — GNS CRI

- **Source:** GNS Science (Crown Research Institute) — Groundwater
- **API:** `https://data.gns.cri.nz` / `https://ggw.gns.cri.nz`
- **Class:** `gwml2.harvesters.harvester.gns_cri.GnsCri`

## Data Collected

- Well general information
- Water level measurements

## Notes

Station metadata is fetched via a WFS endpoint returning CSV. Measurements are fetched
from a separate GGW (Groundwater) endpoint per station.