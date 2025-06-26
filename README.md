## Project Links

- 🌐 [Main Website](https://ggis.un-igrac.org)
- 📘 [Documentation](https://kartoza.github.io/IGRAC-GGIS/)


# The Global Groundwater Information System (GGIS)

GGIS is a groundwater information system developed for and funded by UN-IGRAC. The GGIS is an interactive portal for sharing data and information on groundwater resources around the world. It gives access to map layers, documents, and well and monitoring data. It also contains several thematic map viewers.


![image](https://github.com/user-attachments/assets/8da808b0-f11c-4db1-aa8b-e0dafb7757b6)


You can visit the live site here: https://ggis.un-igrac.org

## QUICK INSTALLATION GUIDE

```
git clone https://github.com/kartoza/IGRAC-GGIS.git
cd IGRAC-GGIS
git submodule init
git submodule update
cd deployment
make deploy
```

The web will be available at `http://localhost/`

To stop containers:

```
make kill
```

To stop and delete containers:

```
make rm
```

# Commands

Here is the list command for IGRAC

## generate_data_wells_cache

For generating cache of wells for download file.

### Parameters

```
--id : id of well that will be checked
--from_id : id start of well to be checked
--country_code : country that will be used to filter the wells
--force : use this to regenerate the cache, without it, it will just check if cache if not generated yet
--generator : ['general_information','hydrogeology','management','drilling_and_construction','monitor'] in comma separator
```

## generate_well_measurement_cache

For generating cache of wells for measurements for graph.

### Parameters

```
--id : id of well that will be checked
--measurement_name : name of measurement: WellLevelMeasurement, WellQualityMeasurement, WellYieldMeasurement
--from_id : id start of well to be checked
--country_code : country that will be used to filter the wells
```

## generate_data_countries_cache

For generating cache of country for download file.

### Parameters

```
--country_code : country that will be regenerate
```

## generate_data_organisations_cache

For generating cache of organisations for download file.

### Parameters

```
--id : id of organisation that will be checked
--from_id : id start of organisation to be checked
```

## update_measurement_type

For updating measurement type of well.

### Parameters

```
--form : id start of well to be checked
```

## update_number_of_measurements_well

For updating number of measurement of well.

### Parameters

```
--form : id start of well to be checked
```
