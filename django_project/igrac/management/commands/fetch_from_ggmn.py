# coding=utf-8
import requests
import re
import os
import time
import calendar
from shutil import copyfile
from openpyxl import load_workbook
from geopy.geocoders import Nominatim
from django.core.management.base import BaseCommand

CODE = 'code'
NAME = 'name'
GEOMETRY = 'geometry'
COORDINATES = 'coordinates'
LAT = 'lat'
LON = 'lon'
STATION_TYPE = 'station_type'
WELL_TEMPLATE_FILE = 'WELL_TEMPLATE.xlsx'


class Command(BaseCommand):

    ggmn_station_url = 'https://ggmn.lizard.net/api/v3/groundwaterstations/'
    well_ids = []
    well_data = []
    locator = Nominatim(user_agent='geocoder')
    max_page = 10

    def get_current_timestamp(self):
        """
        Return current timestamp
        """
        gmt = time.gmtime()
        return calendar.timegm(gmt)

    def fetch_wells(self, well_template_output_path, page=1):
        """
        Fetch wells from api
        """
        if page > self.max_page:
            return

        print('#- Processing page {}'.format(page))
        response = requests.get('{base_url}?page={page}'.format(
            base_url=self.ggmn_station_url,
            page=page
        ))
        ground_stations = response.json()

        wb = load_workbook(well_template_output_path)
        ws = wb.worksheets[0]

        for ground_station in ground_stations['results']:
            if ground_station[CODE] in self.well_ids:
                continue
            self.well_ids.append(ground_station[CODE])
            print('#-- Processing well {}'.format(ground_station[CODE]))
            lat = ground_station[GEOMETRY][COORDINATES][1]
            lon = ground_station[GEOMETRY][COORDINATES][0]
            location = self.locator.reverse(
                '{lat},{lon}'.format(
                    lat=lat,
                    lon=lon
                )
            )
            row_data = [
                ground_station[CODE], # ID
                ground_station[NAME], # NAME
                ground_station[STATION_TYPE], # Feature type
                '', # Purpose
                lat, # Lat
                lon, # Lon
                '','','','', # Others
                location.raw['address']['country_code'].upper(),
                location.address,
                '' # Description
            ]
            ws.append(row_data)
        wb.save(well_template_output_path)
        if 'next' in ground_stations:
            next_url = ground_stations['next']
            next_page = int(re.findall(r'\d+', next_url)[-1])
            if next_page <= self.max_page:
                self.fetch_wells(well_template_output_path, next_page)

    def handle(self, *args, **options):
        """Implementation for command.
        :param args:  Not used
        :param options: Not used

        """

        well_template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            WELL_TEMPLATE_FILE
        )
        well_template_output_name = '{file}_{time}.xlsx'.format(
            file='WELL',
            time=self.get_current_timestamp()
        )
        well_template_output_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            well_template_output_name
        )
        copyfile(
            well_template_path,
            well_template_output_path
        )

        self.fetch_wells(well_template_output_path)
