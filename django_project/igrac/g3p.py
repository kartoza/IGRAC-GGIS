import csv
import time
import datetime
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import (
    xframe_options_exempt, xframe_options_sameorigin,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from core.settings.utils import absolute_path  # noqa

xframe_options_exempt_m = method_decorator(
    xframe_options_exempt, name='dispatch')


class G3PTimeseriesChart(View):
    @xframe_options_exempt_m
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        name = kwargs['name']

        return render(
            request,
            'g3p_timeseries_chart.html',
            {
                'id': id,
                'identifier': name
            }
        )


class G3PTimeseriesChartIframe(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        name = kwargs['name']

        return render(
            request,
            'g3p_timeseries_chart_iframe.html',
            {
                'url': reverse('g3p-timeseries-chart', kwargs={
                    'id': id,
                    'name': name
                })
            }
        )


class G3PTimeseriesData(APIView):
    def get(self, request, format=None):
        object_id = request.GET.get('id', None)
        response = {
            'name': request.GET.get('name', 'G3P Timeseries Data'),
            'data': []
        }
        data = []
        if not object_id:
            raise Http404('Missing object id')

        csv_path = absolute_path(
            'igrac',
            'static',
            'csv',
            'GGMN_aquifersSET1.csv'
        )
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row[0] == object_id:
                    try:
                        dt = (
                            time.mktime(
                                datetime.datetime.strptime(row[1],
                                    "%Y-%m-%d %H:%M:%S").timetuple()
                                    )
                        )
                        data.append({
                            'dt': dt,
                            'par': 'Groundwater Storage',
                            'u': 'm',
                            'v': float(row[2])
                        })
                    except:  # noqa
                        pass
        data.sort(key=lambda x: x['dt'], reverse=True)
        response['data'] = data
        return Response(response)
