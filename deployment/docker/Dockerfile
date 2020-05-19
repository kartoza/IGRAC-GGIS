#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM geonode/spcgeonode:django-3.0
MAINTAINER Anita Hapsari<anita@kartoza.com>

ENV HTTP_HOST 0.0.0.0
ENV HTTPS_HOST 0.0.0.0

RUN mkdir -p /usr/share/man/man1
RUN apt-get update -y && apt-get -y --allow-downgrades --allow-remove-essential --allow-unauthenticated install yui-compressor rpl mdbtools git

ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
#
#USER www-data
WORKDIR /home/web/django_project

# Open port 8080 as we will be running our uwsgi socket on that
#EXPOSE 8080

ADD uwsgi.conf /uwsgi.conf
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
