"""
This script initializes Geonode
"""

#########################################################
# Setting up the  context
#########################################################

import datetime
import json
import os
import shutil
import time
import uuid

import django
import requests

django.setup()

#########################################################
# Imports
#########################################################

from django.conf import settings
from django.db import connection
from django.utils import timezone
from django.db.utils import OperationalError
from django.contrib.auth import get_user_model
from django.core.management import call_command
from requests.exceptions import ConnectionError
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, get_application_model

# Getting the secrets
admin_username = os.getenv('ADMIN_USERNAME')
admin_password = os.getenv('ADMIN_PASSWORD')
admin_email = os.getenv('ADMIN_EMAIL')

#########################################################
# 1. Waiting for PostgreSQL
#########################################################

print("-----------------------------------------------------")
print("1. Waiting for PostgreSQL")
for _ in range(60):
    try:
        connection.ensure_connection()
        break
    except OperationalError:
        time.sleep(1)
else:
    connection.ensure_connection()
connection.close()

#########################################################
# 2. Running the migrations
#########################################################

print("-----------------------------------------------------")
print("2. Running the migrations")
call_command('makemigrations')
call_command('migrate', '--noinput')
call_command('migrate', app_label='gwml2', database='gwml2')

#########################################################
# 3. Creating superuser if it doesn't exist
#########################################################

print("-----------------------------------------------------")
print("3. Creating/updating superuser")
try:
    superuser = get_user_model().objects.get(username=admin_username)
    superuser.set_password(admin_password)
    superuser.is_active = True
    superuser.email = admin_email
    superuser.save()
    print('superuser successfully updated')
except get_user_model().DoesNotExist:
    superuser = get_user_model().objects.create_superuser(
        admin_username,
        admin_email,
        admin_password
    )
    print('superuser successfully created')

#########################################################
# 4. Create an OAuth2 provider to use authorisations keys
#########################################################

print("-----------------------------------------------------")
print("4. Create/update an OAuth2 provider to use authorisations keys")

Application = get_application_model()
app, created = Application.objects.get_or_create(
    pk=1,
    name='GeoServer',
    client_type='confidential',
    authorization_grant_type='authorization-code',
)
app.skip_authorization = True
_host = os.getenv('HTTPS_HOST', "") if os.getenv('HTTPS_HOST',
                                                 "") != "" else os.getenv(
    'HTTP_HOST')
_port = os.getenv('HTTPS_PORT') if os.getenv('HTTPS_HOST',
                                             "") != "" else os.getenv(
    'HTTP_PORT', '80')
# default port is 80
_protocols = {
    "80": "http://",
    "443": "https://"
}
if _port not in _protocols:
    redirect_uris = [
        'http://{}:{}/geoserver'.format(_host, _port),
        'http://{}:{}/geoserver/index.html'.format(_host, _port),
    ]
else:
    # Make sure protocol string match with GeoServer Redirect URL's protocol string
    redirect_uris = [
        '{}{}/geoserver'.format(_protocols[_port], _host),
        '{}{}/geoserver/index.html'.format(_protocols[_port], _host),
    ]

app.redirect_uris = "\n".join(redirect_uris)
app.save()
if created:
    print('oauth2 provider successfully created')
else:
    print('oauth2 provider successfully updated')

#########################################################
# 5. Loading fixtures
#########################################################

print("-----------------------------------------------------")
print("5. Loading fixtures")

# Disable fixtures loading in prod by including environment variable:
#  INITIAL_FIXTURES=False
import ast

# To conform with original behaviour of GeoNode, we need to set it to True
# as default value
_load_initial_fixtures = ast.literal_eval(
    os.getenv('INITIAL_FIXTURES', 'True'))
if _load_initial_fixtures:
    call_command('loaddata', 'initial_data')
    call_command('update_fixtures')

#########################################################
# 6. Running updatemaplayerip
#########################################################

print("-----------------------------------------------------")
print("6. Running updatemaplayerip - skip")
# call_command('updatelayers')
#  TODO CRITICAL : this overrides the layer thumbnail of existing layers even if unchanged !!!
# call_command('updatemaplayerip')


#########################################################
# 7. Collecting static files
#########################################################

print("-----------------------------------------------------")
print("7. Collecting static files")
static_root = settings.STATIC_ROOT
if os.path.isdir(static_root):
    shutil.rmtree(static_root)
    os.makedirs(static_root, exist_ok=True)
call_command('collectstatic', '--noinput', verbosity=0)

#########################################################
# 8. Waiting for GeoServer
#########################################################

print("-----------------------------------------------------")
print("8. Waiting for GeoServer")
_geoserver_host = os.getenv('GEOSERVER_LOCATION',
                            'http://geoserver:8080/geoserver')
for _ in range(60 * 5):
    try:
        requests.head("{}".format(_geoserver_host))
        break
    except ConnectionError:
        time.sleep(1)
else:
    requests.head("{}".format(_geoserver_host))

#########################################################
# 9. Securing GeoServer
#########################################################

print("-----------------------------------------------------")
print("9. Securing GeoServer")

geoserver_admin_username = os.getenv('GEOSERVER_ADMIN_USER')
geoserver_admin_password = os.getenv('GEOSERVER_ADMIN_PASSWORD')

# Getting the old password
try:
    r1 = requests.get('{}/rest/security/masterpw.json'.format(_geoserver_host),
                      auth=(
                          geoserver_admin_username, geoserver_admin_password))
except requests.exceptions.ConnectionError:
    print(
        "Unable to connect to GeoServer. Make sure GeoServer is started and accessible.")
    exit(1)
r1.raise_for_status()
old_password = json.loads(r1.text)["oldMasterPassword"]

if old_password == 'M(cqp{V1':
    print("Randomizing master password")
    new_password = uuid.uuid4().hex
    data = json.dumps(
        {"oldMasterPassword": old_password, "newMasterPassword": new_password})
    r2 = requests.put('{}/rest/security/masterpw.json'.format(_geoserver_host),
                      data=data,
                      headers={'Content-Type': 'application/json'}, auth=(
            geoserver_admin_username, geoserver_admin_password))
    r2.raise_for_status()
else:
    print("Master password was already changed. No changes made.")

#########################################################
# 10. Test User Model
#########################################################

print("-----------------------------------------------------")
print("10. Test User Model")


def make_token_expiration(seconds=86400):
    _expire_seconds = getattr(settings, 'ACCESS_TOKEN_EXPIRE_SECONDS', seconds)
    _expire_time = datetime.datetime.now(timezone.get_current_timezone())
    _expire_delta = datetime.timedelta(seconds=_expire_seconds)
    return _expire_time + _expire_delta


user = get_user_model().objects.get(username=admin_username)
expires = make_token_expiration()
(access_token, created) = AccessToken.objects.get_or_create(
    user=user,
    application=app,
    expires=expires,
    token=generate_token())

#########################################################
# 11. Restart harvesters and uploads
#########################################################

try:
    from gwml2.functions import Functions

    print("-----------------------------------------------------")
    print("11. Restart harvesters and uploads")

    Functions().restart_harvesters()
    Functions().restart_uploads()
except Exception as e:
    print(f'{e}')
    pass
