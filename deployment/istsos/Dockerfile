#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM istsos/istsos:2.4.1
MAINTAINER Irwan Fathurrahman<irwan@kartoza.com>

ADD deployment/istsos/services /usr/share/istsos/services
ADD istsos2/istsoslib /usr/share/istsos/istsoslib
ADD istsos2/application_istsoslib.py /usr/share/istsos/application_istsoslib.py