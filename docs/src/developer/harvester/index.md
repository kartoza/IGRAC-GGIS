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

The Harvester system automatically pulls well and monitoring data from
third-party national
APIs and imports it into the `gwml2` database. Each harvester is a
self-contained Python class
that extends `BaseHarvester` and maps the source data to the GWML2 schema.

## Supported Sources

| Country       | Harvester                                   | Data types         |
|---------------|---------------------------------------------|--------------------|
| Argentina     | [Azul BDH](./azul_bdh.md)                   | Level              |
| Austria       | [eHYD](./ehyd.md)                           | Level (file-based) |
| El Salvador   | [SNET](./el_salvador.md)                    | Level              |
| Estonia       | [Keskkonnaportaal](./estonia.md)            | Level              |
| France        | [Hubeau](./hubeau.md)                       | Level, Quality     |
| Germany       | [Lower Saxony](./lower_saxony.md)           | Level              |
| International | [GIN GW-Info](./gin_gw_info.md)             | Level              |
| Ireland       | [EPA Hydronet](./epawebapp.md)              | Level              |
| Netherlands   | [BRO](./netherlands.md)                     | Level, Quality     |
| New Zealand   | [GNS CRI](./gns_cri.md)                     | Level              |
| Norway        | [HydAPI / NVE](./hydapi.md)                 | Level              |
| Norway        | [Miljødirektoratet](./miljodirektoratet.md) | Quality            |
| Rwanda        | [RWB](./rwanda.md)                          | Level              |
| Sweden        | [SGU](./sgu.md)                             | Level              |
| USA           | [CIDA / USGS](./cida.md)                    | Level, Quality     |