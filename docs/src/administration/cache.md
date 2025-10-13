---
title: Documentation
summary: GGIS
  - Lindie Strijdom
  - Irwan Fathurrahman
date: 2025-10-01
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
context_id: nDU6LLGiXPTLADXY
---

# Cache Management

## Overview

The IGRAC system uses several cache types to improve performance and reduce load times. Caching allows data such as wells, countries, and organisations to be served quickly to users.

However, cache generation can be time-consuming and may occasionally fail, leading to outdated or missing data. To address this, clients can manually trigger cache generation directly via the Django Admin interface.

<br>

## Cache Types and Purpose

<br>

| **Cache Category**     | **Cache Type**        | **Description**                                                                                     |
| ---------------------- | --------------------- | --------------------------------------------------------------------------------------------------- |
| **Well Cache**         | *Measurement Cache* | Stores measurement data for generating well graphs quickly.                                         |
|                        | *Data Cache*        | Contains downloadable well data files (e.g., `.ods` format).                                        |
|                        | *Metadata Cache*    | Holds metadata such as the number of measurements, types of wells, and related summary information. |
| **Country Cache**      | *Data Cache*        | Zipped file containing data cache of wells for a specific country.                                  |
| **Organisation Cache** | *Data Cache*        | Zipped file containing data cache of wells for a specific organisation.                             |

<br>

## Django Admin

All cache types can be viewed and managed through the **Django Admin Interface**.

Cache generation can be triggered manually, allowing users to refresh their own data caches without waiting for automated background jobs or developer intervention.

<br>

### Well Cache

**URL:** [Well Cache Admin](https://ggis.un-igrac.org/en-us/admin/gwml2/wellcacheindicator/)

<br>

Each well cache record includes:

- **`Time when measurement cache generated`**
    
    Timestamp when the measurement cache was last created.

    <br>

- **`Time when data cache generated`**

    Timestamp when the data cache was last created.

    <br>

- **`Time when metadata generated`**

    Timestamp when the metadata cache was last created.

    <br>

- **`Data cache information`**

    Timestamp of the actual cache file creation, used to verify that all cache files are properly generated.

<br>

![Well Cache](./img/cache/cache-1.png)

<br>

**To generate a cache:**

1. Select one or more wells from the list.

2. From the dropdown at the bottom-left, select **`Generate data cache`**.

3. Click **Go**.

<br>

![Generate Well Cache](./img/cache/cache-2.png)

<br>

### Country Cache

**URL:** [Country Cache Admin](https://ggis.un-igrac.org/en-us/admin/gwml2/country/)

<br>

Each country record includes:

- **`Time when data cache generated`**
    
    Timestamp when the data cache was last created.

    <br>

- **`Data cache information`**

    Timestamp of the corresponding cache file creation.

<br>

**To generate a cache:**

1. Select one or more countries from the list.

2. From the dropdown at the bottom-left, select **`Generate data cache`**.

3. Click **Go**.

<br>

![Generate Country Cache](./img/cache/cache-3.png)

<br>

### Organisation Cache

**URL:** [Organisation Cache Admin](https://ggis.un-igrac.org/en-us/admin/gwml2/country/)

<br>

Each organisation record includes:

- **`Time when data cache generated`**
    
    Timestamp when the data cache was last created.

    <br>

- **`Data cache information`**

    Timestamp of the cache file creation.

<br>

**To generate a cache:**

1. Select one or more organisations from the list.

2. From the dropdown at the bottom-left, select **`Generate data cache`**.

3. Click **Go**.

<br>

![Generate Organisation Cache](./img/cache/cache-4.png)

<br>

The IGRAC cache system improves data delivery efficiency by pre-generating downloadable files and metadata. Manual cache regeneration empowers clients to refresh outdated caches, ensuring up-to-date and reliable data access without waiting for scheduled background updates.

<br>
