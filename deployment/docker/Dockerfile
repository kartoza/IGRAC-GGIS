#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM geonode/spcgeonode:django-3.0
MAINTAINER Anita Hapsari<anita@kartoza.com>

RUN mkdir -p /usr/share/man/man1
RUN apt-get update -y && apt-get -y --allow-downgrades --allow-remove-essential --allow-unauthenticated install yui-compressor rpl mdbtools git
RUN echo "Activate memcached" && \
    apt-get update && apt-get install -y memcached && \
    pip install pylibmc  && pip install sherlock

WORKDIR /spcgeonode

# TODO: base repo : https://github.com/kartoza/geonode/commit/4f64450061046881aea74ea43673965440318e64
RUN git pull https://github.com/kartoza/geonode.git 3.2.2
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
