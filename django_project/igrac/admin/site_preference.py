import os
import re

from django.conf import settings
from django.contrib import admin
from django.db import connections
from django.http import JsonResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from preferences.admin import PreferencesAdmin

from igrac.models.site_preference import SitePreference

# Objects ordered as in default.sql
ISTSOS_OBJECTS = [
    ('offerings', 'table'),
    ('obs_type', 'table'),
    ('positions', 'view'),
    ('measures', 'view'),
    ('event_time', 'view'),
    ('foi', 'view'),
    ('off_proc', 'view'),
    ('feature_type', 'view'),
    ('observed_properties_sensor', 'materialized view'),
    ('uoms', 'view'),
    ('proc_obs', 'view'),
    ('observed_properties', 'view'),
    ('vw_istsos_sensor', 'view'),
    ('procedures', 'view'),
    ('measures_group', 'materialized view'),
]

_VIEWS_SQL = os.path.normpath(os.path.join(
    os.path.dirname(__file__),
    '..', '..', 'gwml2', 'migrations', 'sql', 'istsos', 'views.sql'
))


def _get_create_sql(name: str):
    """Return all SQL statements in the section that creates istsos.{name}."""
    with open(_VIEWS_SQL) as f:
        content = f.read()
    # Split file into sections delimited by comment headers like "-- EVENT_TIME --"
    parts = re.split(r'(?m)^--[^\n]+--\s*\n', content)
    for part in parts:
        if re.search(rf'\bistsos\.{re.escape(name)}\b', part, re.IGNORECASE):
            # Return each non-empty statement
            return [s.strip() for s in part.split(';') if s.strip()]
    return []


@admin.register(SitePreference)
class CustomPreferencesAdmin(PreferencesAdmin):
    """Custom of preferences admin."""

    readonly_fields = (
        'geonode_version', 'geonode_mapstore_client_version',
        'igrac_version', 'igrac_commit', 'gwml2_version',
        'google_analytic_key', 'istsos_views'
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                'create-istsos-object/<str:name>/',
                self.admin_site.admin_view(self.create_istsos_object_view),
                name='igrac_create_istsos_object',
            ),
        ]
        return custom + urls

    def create_istsos_object_view(self, request, name):
        if request.method != 'POST':
            return JsonResponse(
                {'success': False, 'message': 'Method not allowed'}, status=405
            )
        if not any(n == name for n, _ in ISTSOS_OBJECTS):
            return JsonResponse(
                {'success': False, 'message': f'Unknown object: {name}'}, status=400
            )
        try:
            statements = _get_create_sql(name)
        except FileNotFoundError:
            return JsonResponse(
                {'success': False, 'message': 'views.sql not found'}, status=500
            )
        if not statements:
            return JsonResponse(
                {'success': False, 'message': f'No CREATE statement found for {name}'},
                status=404
            )
        try:
            with connections[settings.GWML2_DATABASE_CONFIG].cursor() as cursor:
                for sql in statements:
                    cursor.execute(sql)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

        return JsonResponse(
            {'success': True, 'message': f'istsos.{name} created successfully'}
        )

    def istsos_views(self, obj):
        """List istsos objects ordered as in default.sql with existence check."""
        existing = set()
        try:
            with connections[settings.GWML2_DATABASE_CONFIG].cursor() as cursor:
                cursor.execute(
                    "SELECT table_name FROM information_schema.views "
                    "WHERE table_schema = 'istsos'"
                )
                existing.update(row[0] for row in cursor.fetchall())
                cursor.execute(
                    "SELECT matviewname FROM pg_matviews "
                    "WHERE schemaname = 'istsos'"
                )
                existing.update(row[0] for row in cursor.fetchall())
                cursor.execute(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = 'istsos' AND table_type = 'BASE TABLE'"
                )
                existing.update(row[0] for row in cursor.fetchall())
        except Exception as e:
            return mark_safe(
                f'<span style="color:red">DB error: {e}</span>'
            )

        rows = []
        for i, (name, obj_type) in enumerate(ISTSOS_OBJECTS, 1):
            if name in existing:
                icon = '<span style="color:green">&#10003;</span>'
            else:
                url = reverse('admin:igrac_create_istsos_object', args=[name])
                icon = (
                    f'<button type="button" '
                    f'style="color:red;background:none;border:none;'
                    f'cursor:pointer;font-size:1em;padding:0;" '
                    f'onclick="createIstsosObject(\'{url}\', \'{name}\', \'{obj_type}\')">'
                    f'&#10007;</button>'
                )
            rows.append(
                f'<tr>'
                f'<td style="padding:4px 8px;color:#666;">{i}</td>'
                f'<td style="padding:4px 8px;font-family:monospace;">istsos.{name}</td>'
                f'<td style="padding:4px 8px;color:#888;">{obj_type}</td>'
                f'<td style="padding:4px 8px;text-align:center;">{icon}</td>'
                f'</tr>'
            )

        table = (
            '<table style="border-collapse:collapse;margin-top:4px;">'
            '<thead><tr>'
            '<th style="padding:4px 8px;text-align:left;border-bottom:1px solid #ccc;">#</th>'
            '<th style="padding:4px 8px;text-align:left;border-bottom:1px solid #ccc;">Name</th>'
            '<th style="padding:4px 8px;text-align:left;border-bottom:1px solid #ccc;">Type</th>'
            '<th style="padding:4px 8px;text-align:left;border-bottom:1px solid #ccc;">Status</th>'
            '</tr></thead>'
            '<tbody>' + ''.join(rows) + '</tbody>'
            '</table>'
        )

        js = """<script>
function createIstsosObject(url, name, type) {
    if (!confirm('Create istsos.' + name + ' (' + type + ')?')) return;
    var csrfToken = document.cookie.match(/csrftoken=([^;]+)/);
    fetch(url, {
        method: 'POST',
        headers: {'X-CSRFToken': csrfToken ? csrfToken[1] : ''},
    })
    .then(function(r) {
        if (!r.ok) {
            return r.text().then(function(text) {
                console.error('[istsos] HTTP ' + r.status, text);
                throw new Error('HTTP ' + r.status);
            });
        }
        return r.json();
    })
    .then(function(data) {
        if (data.success) {
            location.reload();
        } else {
            console.error('[istsos] ' + data.message);
            alert(data.message);
        }
    })
    .catch(function(err) { console.error('[istsos]', err); });
}
</script>
"""
        return mark_safe(js + table)

    istsos_views.short_description = 'ISTSOS Views'