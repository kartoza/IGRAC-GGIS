---
title: El Salvador — SNET
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# El Salvador — SNET

- **Source:** SNET (Servicio Nacional de Estudios Territoriales)
- **API:** `https://srt.snet.gob.sv/apidoa/api/sihi/DataPozos/`
- **Class:** `gwml2.harvesters.harvester.el_savador.base.ElSavadorHarvester`

## Data Collected

- Well general information
- Water level measurements

## Notes

Requires an API key configured as a `HarvesterAttribute` with the name `api-key`.