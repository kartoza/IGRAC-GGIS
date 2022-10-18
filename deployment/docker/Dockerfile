#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM geonode/geonode:3.3.x
MAINTAINER Irwan <irwan@kartoza.com>

RUN mkdir -p /usr/share/man/man1
RUN apt-get update -y && apt-get -y --allow-downgrades --allow-remove-essential --allow-unauthenticated install yui-compressor rpl mdbtools git
RUN echo "Activate memcached" && \
    apt-get update && apt-get install -y memcached && \
    pip install pylibmc  && pip install sherlock

WORKDIR /

RUN rm -r /usr/src/geonode
RUN git clone --branch 3.3.x --single-branch https://github.com/kartoza/geonode.git spcgeonode

WORKDIR /spcgeonode
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
