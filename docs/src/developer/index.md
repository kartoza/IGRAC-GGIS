---
title: Developer Documentation
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Developer Documentation

GGIS is a groundwater information system built on top of **GeoNode**, extended with a dedicated
well and monitoring data platform, a SOS API layer, and an automated harvester system.

This section contains everything a developer needs to understand, run, and contribute to the project.

---

## Contents

- [Project Structure](./project_structure.md) — repository layout, Django apps overview, and submodules
- [Deployment](./deployment.md) — how to run the stack locally, Docker services, Make commands, and management commands
- [GeoNode Customisation](./geonode.md) — IGRAC forks of the GeoNode backend and Mapstore client
- [gwml2](./gwml2.md) — well and monitoring database app (data models, harvesters, forms, download, upload, QC)
- [igrac App](./igrac.md) — main GGIS GeoNode app (UI customisations, models, admin, management commands)
- [igrac_api and istSOS](./igrac_api_and_istsos.md) — SOS 1.0.0 API gateway and istSOS integration
- [Documentation](./documentation.md) — how to run and contribute to this documentation site