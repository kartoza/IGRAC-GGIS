# IGRAC-GGIS

## QUICK INSTALLATION GUIDE

```
git clone https://github.com/kartoza/IGRAC-GGIS.git
cd IGRAC-GGIS/deployment
make build
make up
make collectstatic
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
