#--------- Prod image ------------
FROM geonode/geonode:latest-ubuntu-22.04 AS prod
MAINTAINER Irwan Fathurrahman <irwan@kartoza.com>

ARG CACHE_BUSTER=4
# Set the locale
RUN locale-gen C.UTF-8
ENV LANG C.UTF-8

RUN mkdir -p /usr/share/man/man1
RUN apt-get update -y && apt-get -y --allow-downgrades --allow-remove-essential --allow-unauthenticated install yui-compressor rpl mdbtools git
RUN echo "Activate memcached" && \
    apt-get update && apt-get install -y memcached && \
    pip install pylibmc  && pip install sherlock
RUN apt-get install -y libreoffice

WORKDIR /

ENV GEONODE_VERSION 4.4.1.igrac
RUN rm -r /usr/src/geonode
RUN git clone --branch $GEONODE_VERSION --single-branch https://github.com/kartoza/geonode.git geonode

WORKDIR /geonode

RUN pip install -r requirements.txt
RUN pip uninstall -y django-geonode-mapstore-client

ADD deployment/docker/REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt

# Not sure why we have this migrations
# RUN rm /usr/local/lib/python3.10/dist-packages/avatar/migrations/0002_auto_20200210_1421.py

#USER www-data
ADD django_project /home/web/django_project
WORKDIR /home/web/django_project
RUN rm -rf /home/web/django_project/gwml2

# Installing gwml2
ENV GWML2_VERSION geonode-4.4.1-2
RUN git clone --branch $GWML2_VERSION https://github.com/kartoza/IGRAC-WellAndMonitoringDatabase.git /home/web/django_project/gwml2
RUN echo $GWML2_VERSION > /home/web/django_project/gwml2/version.txt

# Add geonode version
RUN echo $GEONODE_VERSION > /home/web/django_project/version/geonode_version.txt

# Open port 8080 as we will be running our uwsgi socket on that
#EXPOSE 8080

ADD deployment/docker/entrypoint.sh /entrypoint.sh
ADD deployment/docker/initialize.py /initialize.py
ADD deployment/docker/uwsgi.conf /uwsgi.conf
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uwsgi", "--ini", "/uwsgi.conf"]

#--------- Development image ------------
FROM prod AS dev

ADD deployment/docker/REQUIREMENTS-DEV.txt /REQUIREMENTS-DEV.txt
RUN pip install -r /REQUIREMENTS-DEV.txt

# This section taken on 2 July 2015 from
# https://docs.docker.com/examples/running_ssh_service/
# Sudo is needed by pycharm when it tries to pip install packages
RUN apt-get update && apt-get install -y openssh-server sudo
RUN mkdir -p /var/run/sshd
RUN echo 'root:docker' | chpasswd
RUN sed -i 's/^PermitRootLogin */#PermitRootLogin /' /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# --------------------------------------------------------
# Open ports as needed
# --------------------------------------------------------

# Open port 8080 as we will be running our django dev server on
EXPOSE 8080
# Open port 22 as we will be using a remote interpreter from pycharm
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]