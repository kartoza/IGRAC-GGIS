---
title: Documentation  
summary: GGIS  
author: Irwan Fathurrahman  
date: 2025-07-02  
some_url: https://github.com/kartoza/IGRAC-GGIS  
copyright: Copyright 2025, Kartoza  
contact:  
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.  
---

## Contributors

The **Contributors** feature allows you to view the contributors of layers.  
It displays a list of organizations along with their metadata.

![image](./img/contributors/step%201.png)  
![image](./img/contributors/step%202.png)

### How to Set Up

Contributors are based on the IGRAC layers in Django.  

- **Production**: https://ggis.un-igrac.org/en-us/admin/igrac/groundwaterlayer/  
- **Staging**: https://igrac.sta.do.kartoza.com/en-us/admin/igrac/groundwaterlayer/  

These layers represent well and monitoring data, and their variants.  
Contributors are linked to these layers through the organizations and organization groups associated with them.

![image](./img/contributors/step%203.png)

To manage contributor content, update the related organizations:

- **Production**: https://ggis.un-igrac.org/en-us/admin/gwml2/organisation/  
- **Staging**: https://igrac.sta.do.kartoza.com/en-us/admin/gwml2/organisation/

![image](./img/contributors/step%204.png)

### Setting the Time Range

For each organization:

- If it's used by a harvester, it will display: **"Updated automatically (via API)"**
- If not, the time range will be calculated from the first and last measurements

To calculate it manually:

1. Select one or more organizations  
2. Choose the **Assign Data** action from the dropdown  

![image](./img/contributors/step%204.png)
