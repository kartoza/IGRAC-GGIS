#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM geonode/spcgeonode:django-3.0
MAINTAINER Anita Hapsari<anita@kartoza.com>

RUN mkdir -p /usr/share/man/man1
RUN apt-get update -y && apt-get -y --allow-downgrades --allow-remove-essential --allow-unauthenticated install yui-compressor rpl mdbtools git

WORKDIR /spcgeonode

# TODO: base repo : https://github.com/GeoNode/geonode/commit/4f780ebf2744ada788e4b21782d4e6c53bd60e0f
# This is geonode : 3.2 stable version
RUN git pull https://github.com/kartoza/geonode.git geonode.3.2-fix
RUN pip install -r requirements.txt

RUN pip uninstall -y django-geonode-mapstore-client

ADD deployment/docker/REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
#
#USER www-data
ADD django_project /home/web/django_project
WORKDIR /home/web/django_project

# Open port 8080 as we will be running our uwsgi socket on that
#EXPOSE 8080

ADD deployment/docker/entrypoint.sh /entrypoint.sh
ADD deployment/docker/initialize.py /initialize.py
ADD deployment/docker/uwsgi.conf /uwsgi.conf
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
