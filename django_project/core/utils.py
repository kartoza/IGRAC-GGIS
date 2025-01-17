from django.conf import settings
from django.db import connections


def database_monitoring(database: str):
    """Check database connection."""
    try:
        with connections[database].cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
    except Exception as e:
        if "doesn't exist." in str(e):
            raise Exception(
                f'Database does not exist, '
                f'databases are: {list(settings.DATABASES.keys())}'
            )
        else:
            raise e
