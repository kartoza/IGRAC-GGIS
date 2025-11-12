import requests
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


def deepl_translater(text, source_lang=None, target_lang="EN"):
    """Translate text using DeepL."""
    DEEPL_API_KEY = settings.DEEPL_API_KEY
    if not DEEPL_API_KEY:
        raise ValueError("Missing DEEPL_API_KEY")

    data = {
        "text": text,
        "target_lang": target_lang,
        "model_type": "quality_optimized"
    }
    if source_lang:
        data["source_lang"] = source_lang
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
    }
    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        headers=headers,
        data=data
    )
    response.raise_for_status()
    return response.json()["translations"][0]["text"]
