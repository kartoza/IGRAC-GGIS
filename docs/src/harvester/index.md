---
title: Harvester
summary: GGIS
author: Irwan Fathurrahman
date: 2026-05-15
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Harvester

The Harvester system automatically pulls well and monitoring data from third-party national
APIs and imports it into the `gwml2` database. Each harvester is a self-contained Python class
that extends `BaseHarvester` and maps the source data to the GWML2 schema.

## Supported Sources

| Harvester | Country | Data types |
|-----------|---------|-----------|
| [SGU](./sgu.md) | Sweden | Level |
| [Hubeau](./hubeau.md) | France | Level, Quality |
| [CIDA / USGS](./cida.md) | USA | Level, Quality |
| [eHYD](./ehyd.md) | Austria | Level (file-based) |
| [SNET](./el_salvador.md) | El Salvador | Level |
| [Lower Saxony](./lower_saxony.md) | Germany | Level |
| [Miljødirektoratet](./miljodirektoratet.md) | Norway | Quality |
| [HydAPI / NVE](./hydapi.md) | Norway | Level |
| [BRO](./netherlands.md) | Netherlands | Level, Quality |
| [RWB](./rwanda.md) | Rwanda | Level |
| [Keskkonnaportaal](./estonia.md) | Estonia | Level |
| [Azul BDH](./azul_bdh.md) | Argentina | Level |
| [EPA Hydronet](./epawebapp.md) | Ireland | Level |
| [GIN GW-Info](./gin_gw_info.md) | International | Level |
| [GNS CRI](./gns_cri.md) | New Zealand | Level |