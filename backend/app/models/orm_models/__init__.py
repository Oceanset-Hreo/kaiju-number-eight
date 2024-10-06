from typing import List

from geoalchemy2 import functions

from .orm_models import Site, SiteInfo, SuitableCrop


def get_site(site_id):
    site = Site.query.get(site_id)
    return site


def get_sites(latitude, longitude, distance_degree) -> List[SiteInfo]:
    sites = (
        SiteInfo.query.filter(
            functions.ST_Distance(
                functions.ST_GeomFromText(f"POINT({longitude} {latitude})", 4326),
                SiteInfo.geometry,
            )
            < distance_degree
        )
        .order_by(
            functions.ST_Distance(
                functions.ST_GeomFromText(f"POINT({longitude} {latitude})", 4326),
                SiteInfo.geometry,
            )
        )
        .limit(10)
        .all()
    )

    return sites


def get_sutibale_crops(latitude, longitude, distance_degree, crop=None) -> List[SuitableCrop]:

    sutiable_crops = (
        SuitableCrop.query.filter(
            functions.ST_Distance(
                functions.ST_GeomFromText(f"POINT({longitude} {latitude})", 4326),
                SuitableCrop.geometry,
            )
            < distance_degree
        )
        .filter(SuitableCrop.C_level >= 0.6)
        .order_by(
            functions.ST_GeomFromText(f"POINT({longitude} {latitude})", 4326),
        )
        .order_by(SuitableCrop.C_level.desc())
    )

    if crop is not None:
        sutiable_crops = sutiable_crops.filter(SuitableCrop.CRP == crop)

    sutiable_crops = sutiable_crops.all()
    return sutiable_crops[:10]
