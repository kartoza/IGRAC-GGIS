---
title: CIDA / USGS (USA)
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# CIDA / USGS — United States

- **Source:** USGS National Groundwater Monitoring Network (NGWMN)
- **API:** `https://www.usgs.gov/apps/ngwmn/geoserver/ngwmn/wfs`
- **Class:** `gwml2.harvesters.harvester.cida.base.CidaUsgsApi`

## Data Collected

- Well general information (via WFS GetFeature)
- Water level measurements
- Water quality measurements

## Notes

Stations are fetched via a WFS request returning GML2. Individual measurements are
retrieved from `https://cida.usgs.gov/ngwmn/provider/…` per station.