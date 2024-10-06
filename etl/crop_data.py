import os
import polars as pl
import padas as pd
import requests
from sqlalchemy import create_engine
from shapely.geometry import Point
import geopandas as gpd

SQLALCHEMY_DATABASE_URI = ''
base_path = '/Users/{user_name}/Downloads/crop_data/'
for _, _, paths in os.walk(base_path):
    df = pl.DataFrame()
    for path in paths:
        if '2050' not in path:
            continue
        now_path = base_path + path
        new_df = pl.read_csv(now_path, ignore_errors=True)
        new_df = new_df[['ADM1', 'CTR', 'ADMIN1_NAME', 'CRP', 'EXTENTS', 'SUIT_VS', 'SUIT_S', 'SUIT_MS', 'SUIT_mS', 'SUIT_vmS', 'SUIT_NS', 'PROD_VS', 'PROD_S', 'PROD_MS', 'PROD_mS', 'PROD_vmS']]
        df = pl.concat([df, new_df])

drop_du_df = df.unique(subset=["ADM1", "ADMIN1_NAME", "CTR", "CRP"])

level_df = drop_du_df.with_columns(((pl.col("SUIT_VS")) / pl.col('EXTENTS') * 100).alias("A_level"))
level_df = level_df.with_columns(((pl.col("SUIT_VS") + pl.col('SUIT_S')) / pl.col('EXTENTS') * 100).alias("B_level"))
level_df = level_df.with_columns(((pl.col("SUIT_VS") + pl.col('SUIT_S') + pl.col('SUIT_MS')) / pl.col('EXTENTS') * 100).alias("C_level"))
level_df = level_df.with_columns(((pl.col("SUIT_VS") + pl.col('SUIT_S') + pl.col('SUIT_MS') + pl.col('SUIT_mS')) / pl.col('EXTENTS') * 100).alias("D_level"))
level_df = level_df.with_columns(((pl.col("SUIT_VS") + pl.col('SUIT_S') + pl.col('SUIT_MS') + pl.col('SUIT_mS') + pl.col('SUIT_vmS')) / pl.col('EXTENTS') * 100).alias("E_level"))


def get_destination(search_text):
    token = ''
    url_base = f'https://api.mapbox.com/search/geocode/v6/forward?q={search_text}&access_token={token}'

    resp = requests.get(url_base)
    resp_json = resp.json()

    return resp_json


map_list = []
fail_list = []

for location in set(level_df['ADMIN1_NAME']):
    try:
        geo = get_destination(location)['features'][0]['geometry']
    except:
        fail_list.append(location)
        print(f'!!!!{location} failed!!!!')

    map_list.append(
        {
            'ADMIN1_NAME': location,
            'geometry': geo
        }
    )

    print(location, geo)

map_df = pd.DataFrame(map_list)
map_df['geometry'] = map_df['geometry'].apply(lambda x: Point(x['coordinates']))
map_df = gpd.GeoDataFrame(map_df, crs='EPSG:4326', geometry=map_df['geometry'])

level_pd_df = level_df.to_pandas()

prod_df = map_df.merge(level_pd_df, how='left', on='ADMIN1_NAME')

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
with engine.connect() as conn:
    prod_df.to_postgis(
        name='production_data',
        con=conn,
        if_exists='replace',
        index=False,
    )
