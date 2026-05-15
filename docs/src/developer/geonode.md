---
title: GeoNode Customisation
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# GeoNode Customisation

GGIS does not use the upstream GeoNode packages directly. Both the **GeoNode backend** and the
**GeoNode Mapstore frontend client** are replaced with IGRAC-maintained forks.

---

## GeoNode Backend (submodule)

Source: [github.com/kartoza/geonode — branch 4.4.3.igrac](https://github.com/kartoza/geonode/tree/4.4.3.igrac)

The GeoNode backend fork is included as a Git submodule at `geonode/` in the repository root.
It is cloned into the Docker image at build time (see `deployment/docker/Dockerfile`) and
replaces the upstream GeoNode installation entirely.

Changes in this fork are patches that cannot be applied from the outside via Django's
extension points — template overrides, signal hooks, or settings — and therefore had to be
made directly in the GeoNode source.

---

## GeoNode Mapstore Client (pip package)

Source: [github.com/kartoza/geonode-mapstore-client — branch 4.4.3-igrac](https://github.com/kartoza/geonode-mapstore-client/tree/4.4.3-igrac)

The Mapstore client is the React/Mapstore2-based frontend that GeoNode uses for the map
viewer, layer detail pages, and dashboards.

GGIS replaces the upstream package with the IGRAC fork, installed directly from GitHub
in `deployment/docker/REQUIREMENTS.txt`:

```
git+https://github.com/kartoza/geonode-mapstore-client.git@4.4.3-igrac
```

The Dockerfile explicitly uninstalls the upstream version first to ensure the fork takes
precedence:

```dockerfile
RUN pip uninstall -y django-geonode-mapstore-client
```

Customisations in this fork include IGRAC-specific UI changes to the map viewer and
related frontend pages that cannot be achieved through GeoNode's template override mechanism.

---

## Keeping Forks Up to Date

Both forks are pinned to a specific branch/tag. To update them:

- **GeoNode backend** — update the `GEONODE_VERSION` build arg in
  `deployment/docker/Dockerfile` and point the `geonode` submodule to the new commit.
- **Mapstore client** — update the Git ref in `deployment/docker/REQUIREMENTS.txt`
  (e.g. change `@4.4.3-igrac` to the new tag), then rebuild with `make build`.