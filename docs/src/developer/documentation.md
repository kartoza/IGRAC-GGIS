---
title: Documentation
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Documentation (`docs/`)

The documentation for GGIS is built with **MkDocs** using the Material theme.
The source lives in the `docs/` directory of the repository.

---

## Directory Structure

```
docs/
├── src/                        # Markdown source files
│   ├── index.md                # Home page
│   ├── administration/         # Admin guides
│   ├── developer/              # Developer guides (you are here)
│   └── harvester/              # Harvester integration guides
├── assets/                     # Shared images and static files
├── templates/                  # MkDocs HTML template overrides
├── mkdocs-base.yml             # Shared MkDocs config (nav, extensions)
├── mkdocs-html.yml             # HTML build config (inherits base)
├── mkdocs-pdf.yml              # PDF build config (inherits base)
├── mkdocs.yml                  # Default config used by mkdocs serve
├── build-docs-html.sh          # Script to build the HTML site
├── build-docs-pdf.sh           # Script to build the PDF
└── requirements.txt            # Python dependencies for building docs
```

---

## Running Locally

Install dependencies and start the live-reload server:

```bash
cd docs
pip install -r requirements.txt
mkdocs serve
```

The site will be available at `http://localhost:8000`.

---

## Building

Build the static HTML site:

```bash
cd docs
bash build-docs-html.sh
```

Output goes to `docs/site/`. The CI pipeline publishes this to GitHub Pages automatically
on every push to `main`.

---

## Adding a Page

1. Create a new `.md` file under the relevant `src/` subdirectory.
2. Add the frontmatter block (copy from an existing file — `title`, `summary`, `author`,
   `date`, `copyright`, `license`).
3. Register the page in the `nav:` section of `mkdocs-base.yml`.

---

## Navigation Config

Navigation is defined in `docs/mkdocs-base.yml` under the `nav:` key.
Both the HTML and PDF builds inherit from this file, so a single edit keeps both outputs
in sync.