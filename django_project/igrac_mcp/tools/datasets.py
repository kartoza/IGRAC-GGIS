import requests
from asgiref.sync import sync_to_async
from django.conf import settings

from igrac_mcp.server import mcp


def _parse_owner(owner: dict) -> dict:
    return {
        "username": owner.get("username"),
        "first_name": owner.get("first_name"),
        "last_name": owner.get("last_name"),
        "email": owner.get("email"),
        "avatar": owner.get("avatar"),
    }


def _parse_attribute_set(attrs: list) -> list:
    return [
        {
            "name": a.get("attribute"),
            "label": a.get("label") or a.get("attribute_label"),
            "type": a.get("attribute_type"),
            "visible": a.get("visible"),
        }
        for a in attrs
    ]


def _parse_links(links: list) -> dict:
    result = {"services": [], "downloads": [], "metadata": []}
    for link in links:
        entry = {"name": link.get("name"), "url": link.get("url"), "mime": link.get("mime")}
        lt = link.get("link_type", "")
        if lt in ("OGC:WMS", "OGC:WFS", "OGC:WCS"):
            result["services"].append({**entry, "type": lt})
        elif lt == "data":
            result["downloads"].append({**entry, "extension": link.get("extension")})
        elif lt == "metadata":
            result["metadata"].append(entry)
    return result


@mcp.tool()
async def get_dataset_features(
    dataset_id: int,
    page: int = 1,
    page_size: int = 50,
) -> dict:
    """Retrieve features (actual data rows) for a GeoNode dataset via WFS.

    Returns GeoJSON-style features including geometry and properties.

    Args:
    - dataset_id: the numeric ID of the dataset
    - page: page number (default: 1)
    - page_size: number of features per page (default: 50, max: 200)
    """
    def _fetch():
        # Get alternate (typename) from dataset API
        api_url = f"{settings.SITEURL.rstrip('/')}/api/v2/datasets/{dataset_id}"
        meta = requests.get(api_url, timeout=30)
        if meta.status_code == 404:
            return {"error": f"Dataset {dataset_id} not found"}
        meta.raise_for_status()
        ds = meta.json().get("dataset", {})
        typename = ds.get("alternate")
        if not typename:
            return {"error": "Dataset has no alternate (typename)"}

        # Fetch features from GeoServer WFS
        size = min(page_size, 200)
        offset = (page - 1) * size
        wfs_url = f"{settings.GEOSERVER_LOCATION.rstrip('/')}/ows"
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "typeName": typename,
            "outputFormat": "application/json",
            "count": size,
            "startIndex": offset,
        }
        resp = requests.get(wfs_url, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return {
            "total": data.get("numberMatched") or data.get("totalFeatures"),
            "page": page,
            "page_size": size,
            "features": [
                {
                    "id": f.get("id"),
                    "geometry": f.get("geometry"),
                    "properties": f.get("properties"),
                }
                for f in data.get("features", [])
            ],
        }

    return await sync_to_async(_fetch)()


@mcp.tool()
async def get_datasets(
    title: str = "",
    page: int = 1,
    page_size: int = 20,
) -> dict:
    """List GeoNode datasets with basic metadata.

    Args:
    - title: filter by title (case-insensitive, partial match)
    - page: page number (default: 1)
    - page_size: number of results per page (default: 20, max: 100)
    """
    def _fetch():
        url = f"{settings.SITEURL.rstrip('/')}/api/v2/datasets/"
        params: dict = {
            "page": page,
            "page_size": min(page_size, 100),
        }
        if title:
            params["filter{title.icontains}"] = title
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return {
            "total": data.get("total"),
            "page": data.get("page"),
            "page_size": data.get("page_size"),
            "results": [
                {
                    "pk": ds.get("pk"),
                    "title": ds.get("title"),
                    "subtype": ds.get("subtype"),
                    "category": ds.get("category"),
                    "extent": ds.get("extent"),
                    "created": ds.get("created"),
                    "last_updated": ds.get("last_updated"),
                    "is_published": ds.get("is_published"),
                    "thumbnail_url": ds.get("thumbnail_url"),
                    "detail_url": ds.get("detail_url"),
                    "owner": ds.get("owner", {}).get("username"),
                }
                for ds in data.get("datasets", [])
            ],
        }

    return await sync_to_async(_fetch)()


@mcp.tool()
async def get_dataset(dataset_id: int) -> dict:
    """Retrieve detail information for a GeoNode dataset.

    Returns metadata, spatial extent, attributes, OGC service links,
    and download links for the given dataset.

    Args:
    - dataset_id: the numeric ID of the dataset (e.g. 34)
    """
    def _fetch():
        url = f"{settings.SITEURL.rstrip('/')}/api/v2/datasets/{dataset_id}"
        params = {"api_preset": ["viewer_common", "dataset_viewer"]}
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 404:
            return {"error": f"Dataset {dataset_id} not found"}
        response.raise_for_status()
        ds = response.json().get("dataset", {})
        return {
            "pk": ds.get("pk"),
            "uuid": ds.get("uuid"),
            "title": ds.get("title"),
            "abstract": ds.get("abstract"),
            "resource_type": ds.get("resource_type"),
            "subtype": ds.get("subtype"),
            "language": ds.get("language"),
            "created": ds.get("created"),
            "last_updated": ds.get("last_updated"),
            "date": ds.get("date"),
            "date_type": ds.get("date_type"),
            "temporal_extent_start": ds.get("temporal_extent_start"),
            "temporal_extent_end": ds.get("temporal_extent_end"),
            "category": ds.get("category"),
            "keywords": [kw.get("name") for kw in ds.get("keywords", [])],
            "regions": [r.get("name") for r in ds.get("regions", [])],
            "extent": ds.get("extent"),
            "owner": _parse_owner(ds.get("owner", {})),
            "is_published": ds.get("is_published"),
            "is_approved": ds.get("is_approved"),
            "thumbnail_url": ds.get("thumbnail_url"),
            "detail_url": ds.get("detail_url"),
            "embed_url": ds.get("embed_url"),
            "attribution": ds.get("attribution"),
            "supplemental_information": ds.get("supplemental_information"),
            "attribute_set": _parse_attribute_set(ds.get("attribute_set", [])),
            "links": _parse_links(ds.get("links", [])),
            "download_urls": ds.get("download_urls", []),
        }

    return await sync_to_async(_fetch)()