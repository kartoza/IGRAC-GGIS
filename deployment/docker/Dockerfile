#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM geonode/spcgeonode:django-3.0
MAINTAINER Anita Hapsari<anita@kartoza.com>

RUN mkdir -p /usr/share/man/man1
RUN apt-get update -y && apt-get -y --allow-downgrades --allow-remove-essential --allow-unauthenticated install yui-compressor rpl mdbtools git

RUN pip uninstall -y django-geonode-client
RUN pip uninstall -y django-geonode-mapstore-client

WORKDIR /spcgeonode
RUN git pull origin 25d184a10ab4e2c687bd5f6234e054385076d3e1
# TODO:
#   this is used by staging
#   https://github.com/GeoNode/geonode/tree/25d184a10ab4e2c687bd5f6234e054385076d3e1
#   we need to bump it to 3.1

ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
#
#USER www-data
WORKDIR /home/web/django_project

# Open port 8080 as we will be running our uwsgi socket on that
#EXPOSE 8080

ADD entrypoint.sh /entrypoint.sh
ADD initialize.py /initialize.py
ADD uwsgi.conf /uwsgi.conf
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
