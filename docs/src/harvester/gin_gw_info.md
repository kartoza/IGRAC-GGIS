---
title: GIN GW-Info (International)
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# GIN GW-Info — International

- **Source:** Groundwater Information Network (GIN)
- **API:** `https://gin.gw-info.net/GinService/sos/gw` (OGC SOS 2.0)
- **Class:** `gwml2.harvesters.harvester.gin_gw_info.GinGWInfo`

## Data Collected

- Well general information (via SOS GetFeatureOfInterest)
- Water level measurements (via SOS GetObservation)

## Notes

Uses the OGC Sensor Observation Service (SOS) 2.0 protocol. Responses are XML and parsed
with Python's `xml.etree.ElementTree`.