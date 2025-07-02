---
title: Documentation
summary: GGIS
  - Irwan Fathurrahman
date: 2025-07-02
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
---

# Geonode Popup

**Geonode Popup** is a feature that displays content from a Wagtail **Rich Text
** field on a Geonode page.
It can appear on **maps**, **datasets**, **geostories**, and **documents**.

Here’s an example:

![image](./img/geonode_popup/step%207.png)

## How to Set It Up

To use this feature, you need to create a **Geonode Page** in the Wagtail
admin.

### 1. Go to Wagtail Admin

![image](./img/geonode_popup/step%201.png)

### 2. Open the Pages List

Make sure you're on the **root page**.
Click **Pages** in the sidebar. A slide-out menu will appear — click **Pages**
at the top.

![image](./img/geonode_popup/step%202.png)

### 3. Click “Add Child Page”

![image](./img/geonode_popup/step%203.png)

### 4. Select “Geonode Page”

Choose the **Geonode Page** type — this is required for the popup to work.

> ⚠️ Make sure not to select the wrong type!

![image](./img/geonode_popup/step%204.png)

### 5. Fill Out the Form

Complete the fields in the form:

1. **Title** – Any title you like.
2. **Intro** – Optional intro text (not used in the popup).
3. **Body** – This is the **Rich Text field** that will appear in the popup.
4. **Maps** – Select the maps where this popup should appear.
5. **Datasets** – Select the datasets that will use this popup.
6. **Documents** – Select the documents linked to this popup.
7. **Geostories** – Select the geostories where the popup will be shown.

![image](./img/geonode_popup/step%205.png)

### 6. Publish the Page

Click the **“arrow up”** icon, then click **“Publish”**.

![image](./img/geonode_popup/step%206.png)

### ✅ The Popup Is Ready!

You can now view the popup on the selected **map**, **dataset**, **geostory**,
or **document**.

![image](./img/geonode_popup/step%207.png)

Here’s your updated section for **Multiple Content** and **Ordering**, with
improved grammar, structure, and clarity:

## Multiple Content

You can assign **multiple pages** to a single map (or dataset, document, or
geostory).
All associated pages will appear **in order** in the popup, separated by
newlines.

To do this, simply follow the same setup steps as before.
Even if a resource (map, dataset, etc.) is already assigned to another page,
you can still assign it to additional pages.

![image](./img/geonode_popup/step%208.png)

## Ordering Multiple Contents

If a resource (map, dataset, document, or geostory) has **multiple popups**,
you can customize their **display order**.

Here’s how:

### 1. Go to Wagtail Admin

![image](./img/geonode_popup/step%201.png)

### 2. Open the Pages List

Make sure you're in the **root page**.
Click **Pages** in the sidebar. A slide-out menu will appear — click **Pages**
at the top.

![image](./img/geonode_popup/step%202.png)

### 3. Reorder Pages

To change the order:

1. Click the **three dots** at the top-right of the page list.
2. Select **“Sort menu order”**.

![image](./img/geonode_popup/step%209.png)

You’ll see **drag handles (dots)** appear next to each page.

![image](./img/geonode_popup/step%2010.png)

Use **drag-and-drop** to reorder the pages.

> 💡 The order saves automatically after you move an item.

### 4. Confirm the Order

Visit the map (or dataset, document, or geostory) and confirm the popups appear
in the correct order.

![image](./img/geonode_popup/step%2011.png)