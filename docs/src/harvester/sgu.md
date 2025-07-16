---
title: Documentation
summary: GGIS
author: Irwan Fathurrahman
date: 2025-07-16
some_url: https://github.com/kartoza/IGRAC-GGIS
copyright: Copyright 2025, Kartoza
contact:
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.  
---

# SGU

**SGU** is a harvester used to collect groundwater data  
from [SGU Sweden](https://www.sgu.se/).  
The data is categorized into three types: **Water Level**, **Water Quality**,
and **Springs**.

---

## Water Level

Water level data can be referenced from SGU’s main page:  
👉 [
`https://www.sgu.se/grundvatten/grundvattennivaer/matstationer`](https://www.sgu.se/grundvatten/grundvattennivaer/matstationer)

### Getting Stations

The list of wells to be fetched is available via this API:  
👉 [
`https://apps.sgu.se/grundvattennivaer-rest/stationer`](https://apps.sgu.se/grundvattennivaer-rest/stationer)

### Getting Measurements for Each Well

Use the following API endpoint to fetch water level data for a specific
station:

```http
https://resource.sgu.se/oppnadata/grundvatten/api/grundvattennivaer/nivaer/station/{{station_id}}?format=json
```

**Important Fields:**

* `datum_for_matning` → Date of measurement
* `grundvattenniva_m_o.h.` → Groundwater level (in meters above sea level)

## Water Quality

Water quality data can be referenced from SGU’s main page:  
👉 [
`https://www.sgu.se/grundvatten/miljoovervakning-av-grundvatten/kartvisare-och-diagram-for-miljoovervakning-av-grundvattenkemi/`](https://www.sgu.se/grundvatten/miljoovervakning-av-grundvatten/kartvisare-och-diagram-for-miljoovervakning-av-grundvattenkemi/)

### Getting Stations

To fetch stations for water quality monitoring, use:

```http
https://resource.sgu.se/oppnadata/grundvatten/api/miljoovervakning/stationer/{{lanskod}}?format=json
```

> The system loops through all available `lanskod` values.

### Getting Measurements for Each Well

Use the following API to get measurement data for a station:

```http
https://resource.sgu.se/oppnadata/grundvatten/api/miljoovervakning/station/{{station_id}}?format=json
```

**Important Fields:**

* `provtagningsdatum` → Date of measurement
* `paramnamn_kort` → Parameter name
* `matvardetal` → Value
* `enhet` → Unit

### List of Measurements

To fetch the correct parameter, create a new parameter in your system using the
exact value found in `paramnamn_kort`.

| paramnamn_kort               | paramnamn                                              | unit      |
|------------------------------|--------------------------------------------------------|-----------|
| ACENAFTEN                    | Acenaften                                              | µg/l      |
| ACENAFTYLEN                  | Acenaftylen                                            | µg/l      |
| AL                           | Aluminium                                              | mg/l      |
| ALK                          | Alkalinitet                                            | mg HCO3/l |
| AMIDOSULFURON                | Amidosulfuron                                          | µg/l      |
| AMPA                         | AMPA                                                   | µg/l      |
| ANTRACEN                     | Antracen                                               | µg/l      |
| AS                           | Arsenik                                                | µg/l      |
| ATRAZIN                      | Atrazin                                                | µg/l      |
| ATRAZINDESISOPROPYL          | Atrazindesisopropyl                                    | µg/l      |
| ATRAZIN_DESETYL_DESISOPROPYL | Atrazin-desetyl-desisopropyl                           | µg/l      |
| AZOXYSTROBIN                 | Azoxystrobin                                           | µg/l      |
| B                            | Bor                                                    | µg/l      |
| BA                           | Barium                                                 | µg/l      |
| BAM                          | 2,6-Diklorbensamid, BAM                                | µg/l      |
| BENSEN                       | Bensen                                                 | µg/l      |
| BENSO_A_ANTRACEN             | Benso(a)antracen                                       | µg/l      |
| BENSO_A_PYREN                | Benso(a)pyren                                          | µg/l      |
| BENSO_BK_FLUORANTEN          | Benso(bk)fluoranten                                    | µg/l      |
| BENSO_GHI_PERYLEN            | Benso(ghi)perylen                                      | µg/l      |
| BENTAZON                     | Bentazon                                               | µg/l      |
| BIFENOX                      | Bifenox                                                | µg/l      |
| BITERTANOL                   | Bitertanol                                             | µg/l      |
| BOSKALID                     | Boskalid                                               | µg/l      |
| BROMBENSEN                   | Brombensen                                             | µg/l      |
| BROMDIKLORMETAN              | Bromdiklormetan                                        | µg/l      |
| BROMKLORMETAN                | Bromklormetan                                          | µg/l      |
| BUTYLBENSEN                  | n-Butylbensen                                          | µg/l      |
| BUTYLBENSEN_SEC              | sec-Butylbensen                                        | µg/l      |
| BUTYLBENSEN_TERT             | tert-Butylbensen                                       | µg/l      |
| CA                           | Kalcium                                                | mg/l      |
| CD                           | Kadmium                                                | µg/l      |
| CL_JON                       | Klorid                                                 | mg/l      |
| CO                           | Kobolt                                                 | µg/l      |
| CR                           | Krom                                                   | µg/l      |
| CU                           | Koppar                                                 | µg/l      |
| CYANAZIN                     | Cyanazin                                               | µg/l      |
| DEA                          | Atrazindesetyl                                         | µg/l      |
| DESFENYLKLORIDAZON           | Desfenylkloridazon                                     | µg/l      |
| DETA                         | Terbutylazindesetyl                                    | µg/l      |
| DIBENSO_AH_ANTRACEN          | Dibenso(ah)antracen                                    | µg/l      |
| DIBROMETAN_12                | 1,2-Dibromoetan                                        | mg/l      |
| DIBROMKLORMETAN              | Dibromklormetan                                        | µg/l      |
| DIBROMMETAN                  | Dibrommetan                                            | µg/l      |
| DIKLORBENSEN_12              | 1,2-Diklorbensen                                       | µg/l      |
| DIKLORBENSEN_13              | 1,3 Diklorbensen                                       | µg/l      |
| DIKLORBENSEN_14              | 1,4-Diklorbensen                                       | µg/l      |
| DIKLORETAN_11                | 1,1-Dikloretan                                         | µg/l      |
| DIKLORETAN_12                | 1,2-Dikloretan                                         | µg/l      |
| DIKLORETEN_11                | 1,1-Dikloreten                                         | µg/l      |
| DIKLORETEN_12_CIS            | cis 1,2 Dikloreten                                     | µg/l      |
| DIKLORETEN_12_TRANS          | Trans-1,2-Dikloreten                                   | µg/l      |
| DIKLORMETAN                  | Diklormetan                                            | µg/l      |
| DIKLORPROP                   | Diklorprop                                             | µg/l      |
| DIKLORPROPAN_12              | 1,2-Diklorpropan                                       | µg/l      |
| DIKLORPROPAN_13              | 1,3-Diklorpropan                                       | µg/l      |
| DIKLORPROPAN_22              | 2,2-Diklorpropan                                       | µg/l      |
| DIKLORPROPEN_11              | 1,1-Diklorpropen                                       | µg/l      |
| DIKLORPROPEN_CIS_13          | cis-1,3-Diklorpropen                                   | µg/l      |
| DIKLORPROPEN_TRANS_13        | trans-1,3-Diklorpropen                                 | µg/l      |
| DIMETOAT                     | Dimetoat                                               | µg/l      |
| DIURON                       | Diuron                                                 | µg/l      |
| DMS                          | Dimetylsulfamid, DMS                                   | µg/l      |
| DMST                         | DMST                                                   | µg/l      |
| D_24                         | 2,4-Diklorfenoxiättiksyra                              | µg/l      |
| ETOFUMESAT                   | Etofumesat                                             | µg/l      |
| ETU                          | Etylentiourea, ETU                                     | µg/l      |
| ETYLBENSEN                   | Etylbensen                                             | µg/l      |
| F                            | Fluorid                                                | mg/l      |
| FE                           | Järn                                                   | mg/l      |
| FENANTREN                    | Fenantren                                              | µg/l      |
| FENOXAPROP                   | Fenoxaprop                                             | µg/l      |
| FLUOPIKOLID                  | Fluopikolid                                            | µg/l      |
| FLUORANTEN                   | Fluoranten                                             | µg/l      |
| FLUOREN                      | Fluoren                                                | µg/l      |
| FLUOROTRIKLORMETAN           | Fluorotriklormetan/Fluortriklormetan, CFC 11, Freon 11 | µg/l      |
| FLUROXIPYR                   | Fluroxipyr                                             | µg/l      |
| FTS_6_2                      | 6:2 Fluorotelomer sulfonat                             | ng/l      |
| GLYFOSAT                     | Glyfosat                                               | µg/l      |
| HEXAKLORBUTADIEN             | Hexaklorbutadien                                       | µg/l      |
| HG                           | Kvicksilver                                            | µg/l      |
| HYDROXYATRAZIN               | Hydroxyatrazin                                         | µg/l      |
| IMIDAKLOPRID                 | Imidakloprid                                           | µg/l      |
| INDENO_123CD_PYRENE          | Indeno(1,2,3-cd)pyren                                  | µg/l      |
| ISOPROPYLTOLUEN_P            | p-isopropyltoluen                                      | µg/l      |
| ISOPROTURON                  | Isoproturon                                            | µg/l      |
| K                            | Kalium                                                 | mg/l      |
| KARBENDAZIM                  | Karbendazim (Carbendazim)                              | µg/l      |
| KLOPYRALID                   | Klopyralid                                             | µg/l      |
| KLORIDAZON                   | Kloridazon                                             | µg/l      |
| KLORTOULEN_2                 | 2-klortoluen                                           | µg/l      |
| KLORTOULEN_4                 | 4-klortoluen                                           | µg/l      |
| KONDL25                      | Konduktivitet                                          | mS/m      |
| KRYSEN                       | Krysen                                                 | µg/l      |
| KVINMERAK                    | Kvinmerak                                              | µg/l      |
| LINDAN                       | HCH-gamma                                              | µg/l      |
| MCPA                         | MCPA                                                   | µg/l      |
| MEKOPROP                     | Mekoprop                                               | µg/l      |
| METALAXYL                    | Metalaxyl                                              | µg/l      |
| METAMITRON                   | Metamitron                                             | µg/l      |
| METAZAKLOR                   | Metazaklor                                             | µg/l      |
| METRIBUZIN                   | Metribuzin                                             | µg/l      |
| METSULFURONMETYL             | Metsulfuronmetyl                                       | µg/l      |
| MG                           | Magnesium                                              | mg/l      |
| MN                           | Mangan                                                 | mg/l      |
| MO                           | Molybden                                               | µg/l      |
| MONOKLORBENSEN               | Klorbensen                                             | µg/l      |
| NA                           | Natrium                                                | mg/l      |
| NAFTALEN                     | Naftalen                                               | µg/l      |
| NH4_N                        | Ammoniumkväve                                          | mg/l      |
| NI                           | Nickel                                                 | µg/l      |
| NO2_N                        | Nitritkväve                                            | mg/l      |
| NO3_N                        | Nitratkväve                                            | mg/l      |
| O_XYLEN                      | orto-Xylen                                             | ng/l      |
| P                            | Fosfor                                                 | mg/l      |
| PAH_CANCER                   | PAH, summa cancerogena                                 | µg/l      |
| PAH_HOG                      | PAH, summa med hög molekylvikt                         | µg/l      |
| PAH_LAG                      | PAH, summa med låg molekylvikt                         | µg/l      |
| PAH_MEDEL                    | PAH, summa med medelhög molekylvikt                    | µg/l      |
| PAH_OVRIGA                   | PAH, summa övriga                                      | µg/l      |
| PB                           | Bly                                                    | µg/l      |
| PFBA                         | Perfluorbutansyra, PFBA                                | ng/l      |
| PFBS                         | Perfluorbutansulfonat, PFBS                            | ng/l      |
| PFDA                         | Perfluordekansyra, PFDA                                | ng/l      |
| PFDOA                        | Perfluordodekansyra, PFDoA                             | ng/l      |
| PFDOS                        | Perfluordodekansulfonat, PFDoS                         | ng/l      |
| PFDS                         | Perfluordekansulfonat, PFDS                            | ng/l      |
| PFHPA                        | Perfluorheptansyra, PFHpA                              | ng/l      |
| PFHPS                        | Perfluorheptansulfonat, PFHpS                          | ng/l      |
| PFHXA                        | Perfluorhexansyra, PFHxA                               | ng/l      |
| PFHXS                        | Perfluorhexansulfonat, PFHxS                           | ng/l      |
| PFNA                         | Perfluornonansyra, PFNA                                | ng/l      |
| PFNS                         | Perfluornonansulfonat, PFNS                            | ng/l      |
| PFOA                         | Perfluoroktansyra (PFOA)                               | ng/l      |
| PFOS                         | Perfluoroktansulfonsyra                                | ng/l      |
| PFPEA                        | Perfluorpentansyra, PFPeA                              | ng/l      |
| PFPES                        | Perfluorpentansulfonat, PFPeS                          | ng/l      |
| PFTRA                        | Perfluortridekansyra, PFTrA                            | ng/l      |
| PFTRDS                       | Perfluortridekansulfonsyra                             | ng/l      |
| PFUNA                        | Perfluoroundekansyra, PFUnA                            | ng/l      |
| PFUNDS                       | Perfluorundekansulfonsyra                              | ng/l      |
| PH                           | pH                                                     |           |
| PIRIMIKARB                   | Pirimikarb                                             | µg/l      |
| PO4_P                        | Fosfatfosfor                                           | mg/l      |
| PROPAN_12DIBROM_3KLOR        | 1,2-Dibrom-3-klorpropan                                | mg/l      |
| PROPIKONAZOL                 | Propikonazol                                           | µg/l      |
| PROPOXYKARBAZON              | Propoxykarbazon                                        | µg/l      |
| PROPYLBENSEN                 | Propylbensen                                           | µg/l      |
| PROPYLBENSEN_ISO             | iso-Propylbensen                                       | µg/l      |
| PYREN                        | Pyren                                                  | µg/l      |
| SB                           | Antimon                                                | µg/l      |
| SI                           | Kisel                                                  | mg/l      |
| SIMAZIN                      | Simazin                                                | µg/l      |
| SO4                          | Sulfat                                                 | mg/l      |
| SR                           | Strontium                                              | µg/l      |
| STYREN                       | Styren                                                 | mg/l      |
| SUM_PFAS_SLV                 | Summa PFAS SLV 11                                      | ng/l      |
| TEMP_PH                      | Temperatur vid pH-mätning                              | °C        |
| TERBUTRYN                    | Terbutryn                                              | µg/l      |
| TERBUTYLAZIN                 | Terbutylazin                                           | µg/l      |
| TERBUTYLAZIN_2_HYDROXY       | Terbutylazin-2-hydroxy                                 | µg/l      |
| TETRAKLORETAN_1112           | 1,1,1,2-Tetrakloretan                                  | µg/l      |
| TETRAKLORETEN                | Tetrakloreten                                          | µg/l      |
| TETRAKLORMETAN               | Tetraklormetan, koltetraklorid                         | µg/l      |
| TIAMETOXAM                   | Tiametoxam                                             | µg/l      |
| TIFENSULFURONMETYL           | Tifensulfuronmetyl                                     | µg/l      |
| TOC                          | Totalt organiskt kol, TOC                              | mg/l      |
| TOLUEN                       | Toluen                                                 | µg/l      |
| TRIALLAT                     | Triallat                                               | µg/l      |
| TRIBENURONMETYL              | Tribenuronmetyl                                        | µg/l      |
| TRIBROMMETAN                 | Tribrommetan, bromoform                                | µg/l      |
| TRIKLORBENSEN_123            | 1,2,3-Triklorbensen                                    | µg/l      |
| TRIKLORBENSEN_124            | 1,2,4-Triklorbensen                                    | µg/l      |
| TRIKLORETAN_111              | 1,1,1-Trikloretan                                      | µg/l      |
| TRIKLORETAN_112              | 1,1,2-Trikloretan                                      | µg/l      |
| TRIKLORETEN                  | Trikloreten                                            | µg/l      |
| TRIKLORMETAN                 | Triklormetan, kloroform                                | µg/l      |
| TRIKLORPROPAN_123            | 1,2,3-Triklorpropan                                    | µg/l      |
| TRIMETYLBENSEN_124           | 1,2,4-Trimetylbensen                                   | µg/l      |
| TRIMETYLBENSEN_135           | 1,3,5-Trimetylbensen                                   | µg/l      |
| U                            | Uran                                                   | µg/l      |
| V                            | Vanadin                                                | µg/l      |
| VINYLKLORID                  | Vinylklorid                                            | µg/l      |
| XYLEN_M_P                    | meta+para-Xylen                                        | ng/l      |
| ZN                           | Zink                                                   | mg/l      |

## Springs

Springs data can be referenced from SGU’s main page:  
👉 [
`https://apps.sgu.se/kartvisare/kartvisare-kallor.html`](https://apps.sgu.se/kartvisare/kartvisare-kallor.html)

### Getting Stations

The list of wells to be fetched is available via this API:  
👉 [
`https://api.sgu.se/oppnadata/kallor/ogc/features/v1/collections/kallor/items?f=application%2Fvnd.ogc.fg%2Bjson`](https://api.sgu.se/oppnadata/kallor/ogc/features/v1/collections/kallor/items?f=application%2Fvnd.ogc.fg%2Bjson)

**Important Fields:**

* `obsdat` → Date of measurement
* For parameter, we need to setup on the django admin on the Harvester
  parameter maps

![image](./img/sgu%201.png)