---
title: eHYD (Austria)
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# eHYD — Austria

- **Source:** eHYD (Austrian Hydrographical Central Office)
- **Website:** https://ehyd.gv.at
- **Class:** `gwml2.harvesters.harvester.ehyd.file_base.FileBase`

## Data Collected

- Water level measurements

## Notes

Unlike API-based harvesters, eHYD data is delivered as **CSV files pushed directly into
the server** rather than fetched via a live API. The harvester reads these files from a
configured directory on disk and imports the records into the `gwml2` database.