import pandas as pd
from geopandas import GeoDataFrame
from geoalchemy2 import Geometry
from sqlalchemy import create_engine
from shapely.geometry import Point
import requests

import ssl
create_default_context_orig = ssl.create_default_context


def cdc(*args, **kwargs):
    kwargs["purpose"] = ssl.Purpose.SERVER_AUTH
    return create_default_context_orig(*args, **kwargs)


ssl.create_default_context = cdc


SQLALCHEMY_DATABASE_URI = ''
BASE_URL = 'https://api.globe.gov/search/v1/'


def get_measurements(protocol: str, country_code: str = 'TWN', test: bool = True) -> dict:
    url = BASE_URL + 'measurement/protocol/measureddate/country/'

    data = {
        'datefield': 'measuredDate',
        'startdate': '2024-03-01',
        'enddate': '2024-03-01',
        'sample': 'TRUE' if test else 'FALSE',
        'geojson': 'TRUE',
        'countrycode': country_code,
        'protocols': protocol,
    }

    response = requests.get(url, params=data)
    return response.json()


def get_precipitation_monthlies_data(country: str):
    print('get_precipitation_monthlies_data')
    precipitation_monthlies_data = []
    protocol = 'precipitation_monthlies'
    data = get_measurements(protocol, country)
    protocol_data_list = data['features']
    for protocol_data in protocol_data_list:
        new_data = {
            'precipitationmonthliesLiquidAccumulationMm': protocol_data['properties']['precipitationmonthliesLiquidAccumulationMm'],
            'date': protocol_data['properties']['precipitationmonthliesAveragedMonth'],
            'protocol': protocol,
            'country_name': protocol_data['properties']['countryName'],
            'site_name': protocol_data['properties']['siteName'],
            'site_id': protocol_data['properties']['siteId'],
            'elevation': protocol_data['properties']['elevation'],
            'geometry': protocol_data['geometry'],
        }
        precipitation_monthlies_data.append(new_data)

    precipitation_monthlies_df = GeoDataFrame(precipitation_monthlies_data)
    if precipitation_monthlies_df.empty:
        return precipitation_monthlies_df

    df = pd.DataFrame(precipitation_monthlies_data)
    df['geometry'] = df['geometry'].apply(lambda x: Point(x['coordinates']))
    precipitation_monthlies_data_df = GeoDataFrame(df, crs='EPSG:4326', geometry=df['geometry'])

    return precipitation_monthlies_data_df


def get_soil_characterizations_data(country: str):
    print('get_soil_characterizations_data')
    soil_characterizations_data = []

    protocol = 'soil_characterizations'
    data = get_measurements(protocol, country)
    protocol_data_list = data['features']
    for protocol_data in protocol_data_list:
        new_data = {
            'soilcharacterizationsBulkDensityGPerCm3': protocol_data['properties']['soilcharacterizationsBulkDensityGPerCm3'],
            'soilcharacterizationsCarbonates': protocol_data['properties']['soilcharacterizationsCarbonates'],
            'soilcharacterizationsClayPercent': protocol_data['properties']['soilcharacterizationsClayPercent'],
            'soilcharacterizationsHorizonBottomDepthCm': protocol_data['properties']['soilcharacterizationsHorizonBottomDepthCm'],
            'soilcharacterizationsHorizonNumber': protocol_data['properties']['soilcharacterizationsHorizonNumber'],
            'soilcharacterizationsHorizonTopDepthCm': protocol_data['properties']['soilcharacterizationsHorizonTopDepthCm'],
            'soilcharacterizationsMoistureEstimate': protocol_data['properties']['soilcharacterizationsMoistureEstimate'],
            'soilcharacterizationsNitrateEstimate': protocol_data['properties']['soilcharacterizationsNitrateEstimate'],
            'soilcharacterizationsParticleDensityGPerCm3': protocol_data['properties']['soilcharacterizationsParticleDensityGPerCm3'],
            'soilcharacterizationsPh': protocol_data['properties']['soilcharacterizationsPh'],
            'soilcharacterizationsPhMethod': protocol_data['properties']['soilcharacterizationsPhMethod'],
            'soilcharacterizationsPhosphateEstimate': protocol_data['properties']['soilcharacterizationsPhosphateEstimate'],
            'soilcharacterizationsPorosityPercent': protocol_data['properties']['soilcharacterizationsPorosityPercent'],
            'soilcharacterizationsPotassiumEstimate': protocol_data['properties']['soilcharacterizationsPotassiumEstimate'],
            'soilcharacterizationsRockQuantityEstimate': protocol_data['properties']['soilcharacterizationsRockQuantityEstimate'],
            'soilcharacterizationsRootQuantityEstimate': protocol_data['properties']['soilcharacterizationsRootQuantityEstimate'],
            'soilcharacterizationsSandPercent': protocol_data['properties']['soilcharacterizationsSandPercent'],
            'soilcharacterizationsSecondaryColorCode': protocol_data['properties']['soilcharacterizationsSecondaryColorCode'],
            'soilcharacterizationsSiltPercent': protocol_data['properties']['soilcharacterizationsSiltPercent'],
            'soilcharacterizationsStructure': protocol_data['properties']['soilcharacterizationsStructure'],
            'soilcharacterizationsTexture': protocol_data['properties']['soilcharacterizationsTexture'],
            'soilcharacterizationsTextureFieldEstimate': protocol_data['properties']['soilcharacterizationsTextureFieldEstimate'],
            'date': protocol_data['properties']['soilcharacterizationsCollectedOn'],
            'protocol': protocol,
            'country_name': protocol_data['properties']['countryName'],
            'site_name': protocol_data['properties']['siteName'],
            'site_id': protocol_data['properties']['siteId'],
            'elevation': protocol_data['properties']['elevation'],
            'geometry': protocol_data['geometry'],
        }
        soil_characterizations_data.append(new_data)

    soil_characterizations_df = GeoDataFrame(soil_characterizations_data)
    if soil_characterizations_df.empty:
        return soil_characterizations_df

    df = pd.DataFrame(soil_characterizations_data)
    df['geometry'] = df['geometry'].apply(lambda x: Point(x['coordinates']))
    soil_characterizations_data = GeoDataFrame(df, crs='EPSG:4326', geometry=df['geometry'])

    return soil_characterizations_data


def get_soil_phs_data(country: str):
    print('get_soil_phs_data')
    soil_phs_data = []

    protocol = 'soil_phs'
    data = get_measurements(protocol, country)
    protocol_data_list = data['features']
    for protocol_data in protocol_data_list:
        new_data = {
            'soilphsHorizonBottomDepthCm': protocol_data['properties']['soilphsHorizonBottomDepthCm'],
            'soilphsHorizonNumber': protocol_data['properties']['soilphsHorizonNumber'],
            'soilphsHorizonTopDepthCm': protocol_data['properties']['soilphsHorizonTopDepthCm'],
            'soilphsPh': protocol_data['properties']['soilphsPh'],
            'soilphsPhMethod': protocol_data['properties']['soilphsPhMethod'],
            'soilphsReferenceDepthLevel10cm': protocol_data['properties']['soilphsReferenceDepthLevel10cm'],
            'soilphsReferenceDepthLevel30cm': protocol_data['properties']['soilphsReferenceDepthLevel30cm'],
            'soilphsReferenceDepthLevel50cm': protocol_data['properties']['soilphsReferenceDepthLevel50cm'],
            'soilphsReferenceDepthLevel5cm': protocol_data['properties']['soilphsReferenceDepthLevel5cm'],
            'soilphsReferenceDepthLevel60cm': protocol_data['properties']['soilphsReferenceDepthLevel60cm'],
            'soilphsReferenceDepthLevel90cm': protocol_data['properties']['soilphsReferenceDepthLevel90cm'],
            'date': protocol_data['properties']['soilphsCollectedOn'],
            'protocol': protocol,
            'country_name': protocol_data['properties']['countryName'],
            'site_name': protocol_data['properties']['siteName'],
            'site_id': protocol_data['properties']['siteId'],
            'elevation': protocol_data['properties']['elevation'],
            'geometry': protocol_data['geometry'],
        }
        soil_phs_data.append(new_data)

    soil_phs_df = GeoDataFrame(soil_phs_data)
    if soil_phs_df.empty:
        return soil_phs_df

    df = pd.DataFrame(soil_phs_data)
    df['geometry'] = df['geometry'].apply(lambda x: Point(x['coordinates']))
    soil_phs_df = GeoDataFrame(df, crs='EPSG:4326', geometry=df['geometry'])

    return soil_phs_df


def get_soil_fertilities_data(country: str):
    print('get_soil_fertilities_data')
    soil_fertilities_data = []

    protocol = 'soil_fertilities'
    data = get_measurements(protocol, country)
    protocol_data_list = data['features']
    for protocol_data in protocol_data_list:
        new_data = {
            'soilfertilitiesCollectedOn': protocol_data['properties']['soilfertilitiesCollectedOn'],
            'soilfertilitiesComments': protocol_data['properties']['soilfertilitiesComments'],
            'soilfertilitiesHorizonBottomDepthCm': protocol_data['properties']['soilfertilitiesHorizonBottomDepthCm'],
            'soilfertilitiesHorizonNumber': protocol_data['properties']['soilfertilitiesHorizonNumber'],
            'soilfertilitiesHorizonTopDepthCm': protocol_data['properties']['soilfertilitiesHorizonTopDepthCm'],
            'soilfertilitiesNitrateEstimate': protocol_data['properties']['soilfertilitiesNitrateEstimate'],
            'soilfertilitiesPhosphateEstimate': protocol_data['properties']['soilfertilitiesPhosphateEstimate'],
            'soilfertilitiesPotassiumEstimate': protocol_data['properties']['soilfertilitiesPotassiumEstimate'],
            'soilfertilitiesReferenceDepthLevel10cm': protocol_data['properties']['soilfertilitiesReferenceDepthLevel10cm'],
            'soilfertilitiesReferenceDepthLevel30cm': protocol_data['properties']['soilfertilitiesReferenceDepthLevel30cm'],
            'soilfertilitiesReferenceDepthLevel50cm': protocol_data['properties']['soilfertilitiesReferenceDepthLevel50cm'],
            'soilfertilitiesReferenceDepthLevel5cm': protocol_data['properties']['soilfertilitiesReferenceDepthLevel5cm'],
            'soilfertilitiesReferenceDepthLevel60cm': protocol_data['properties']['soilfertilitiesReferenceDepthLevel60cm'],
            'soilfertilitiesReferenceDepthLevel90cm': protocol_data['properties']['soilfertilitiesReferenceDepthLevel90cm'],
            'date': protocol_data['properties']['soilfertilitiesCollectedOn'],
            'protocol': protocol,
            'country_name': protocol_data['properties']['countryName'],
            'site_name': protocol_data['properties']['siteName'],
            'site_id': protocol_data['properties']['siteId'],
            'elevation': protocol_data['properties']['elevation'],
            'geometry': protocol_data['geometry'],
        }
        soil_fertilities_data.append(new_data)

    soil_fertilities_df = GeoDataFrame(soil_fertilities_data)
    if soil_fertilities_df.empty:
        return soil_fertilities_df

    df = pd.DataFrame(soil_fertilities_data)
    df['geometry'] = df['geometry'].apply(lambda x: Point(x['coordinates']))
    soil_fertilities_df = GeoDataFrame(df, crs='EPSG:4326', geometry=df['geometry'])

    return soil_fertilities_df


def get_soil_moisture_for_smap_data(country: str):
    print('get_soil_moisture_for_smap')
    soil_moisture_for_smap_data = []

    protocol = 'soil_moisture_for_smap'
    data = get_measurements(protocol, country)
    protocol_data_list = data['features']
    for protocol_data in protocol_data_list:
        new_data = {
            'soilmoistureforsmapAverageSampleVolumeMl': protocol_data['properties']['soilmoistureforsmapAverageSampleVolumeMl'],
            'soilmoistureforsmapComments': protocol_data['properties']['soilmoistureforsmapComments'],
            'soilmoistureforsmapContainerVolumeMeasuredAt': protocol_data['properties']['soilmoistureforsmapContainerVolumeMeasuredAt'],
            'soilmoistureforsmapDepthLevelCm': protocol_data['properties']['soilmoistureforsmapDepthLevelCm'],
            'soilmoistureforsmapFirstVolumeMeasurement': protocol_data['properties']['soilmoistureforsmapFirstVolumeMeasurement'],
            'soilmoistureforsmapGravimetricSoilMoistureGPerG': protocol_data['properties']['soilmoistureforsmapGravimetricSoilMoistureGPerG'],
            'soilmoistureforsmapSampleBulkDensityGPerMl': protocol_data['properties']['soilmoistureforsmapSampleBulkDensityGPerMl'],
            'soilmoistureforsmapSaturatedFlag': protocol_data['properties']['soilmoistureforsmapSaturatedFlag'],
            'soilmoistureforsmapSoilState': protocol_data['properties']['soilmoistureforsmapSoilState'],
            'soilmoistureforsmapVolumetricSoilMoistureMlPerMl': protocol_data['properties']['soilmoistureforsmapVolumetricSoilMoistureMlPerMl'],
            'date': protocol_data['properties']['soilmoistureforsmapMeasuredAt'],
            'protocol': protocol,
            'country_name': protocol_data['properties']['countryName'],
            'site_name': protocol_data['properties']['siteName'],
            'site_id': protocol_data['properties']['siteId'],
            'elevation': protocol_data['properties']['elevation'],
            'geometry': protocol_data['geometry'],
        }
        soil_moisture_for_smap_data.append(new_data)

    soil_moisture_for_smap_df = GeoDataFrame(soil_moisture_for_smap_data)
    if soil_moisture_for_smap_df.empty:
        return soil_moisture_for_smap_df

    df = pd.DataFrame(soil_moisture_for_smap_data)
    df['geometry'] = df['geometry'].apply(lambda x: Point(x['coordinates']))
    soil_moisture_for_smap_df = GeoDataFrame(df, crs='EPSG:4326', geometry=df['geometry'])

    return soil_moisture_for_smap_df


def get_soil_moisture_via_gravimetrics_data(country: str):
    print('get_soil_moisture_via_gravimetrics')
    soil_moisture_via_gravimetrics_data = []

    protocol = 'soil_moisture_via_gravimetrics'
    data = get_measurements(protocol, country)
    protocol_data_list = data['features']
    for protocol_data in protocol_data_list:
        new_data = {
            'soilmoistureviagravimetricsDepthLevelCm': protocol_data['properties']['soilmoistureviagravimetricsDepthLevelCm'],
            'soilmoistureviagravimetricsMoistureMethod': protocol_data['properties']['soilmoistureviagravimetricsMoistureMethod'],
            'soilmoistureviagravimetricsSaturatedFlag': protocol_data['properties']['soilmoistureviagravimetricsSaturatedFlag'],
            'soilmoistureviagravimetricsSoilState': protocol_data['properties']['soilmoistureviagravimetricsSoilState'],
            'soilmoistureviagravimetricsWaterContentGPerG': protocol_data['properties']['soilmoistureviagravimetricsWaterContentGPerG'],
            'date': protocol_data['properties']['soilmoistureviagravimetricsMeasuredAt'],
            'protocol': protocol,
            'country_name': protocol_data['properties']['countryName'],
            'site_name': protocol_data['properties']['siteName'],
            'site_id': protocol_data['properties']['siteId'],
            'elevation': protocol_data['properties']['elevation'],
            'geometry': protocol_data['geometry'],
        }
        soil_moisture_via_gravimetrics_data.append(new_data)

    soil_moisture_via_gravimetrics_df = GeoDataFrame(soil_moisture_via_gravimetrics_data)
    if soil_moisture_via_gravimetrics_df.empty:
        return soil_moisture_via_gravimetrics_df

    df = pd.DataFrame(soil_moisture_via_gravimetrics_data)
    df['geometry'] = df['geometry'].apply(lambda x: Point(x['coordinates']))
    soil_moisture_via_gravimetrics_df = GeoDataFrame(df, crs='EPSG:4326', geometry=df['geometry'])

    return soil_moisture_via_gravimetrics_df


def get_air_temp_monthlies_data(country: str):
    print('get_air_temp_monthlies')
    air_temp_monthlies_data = []

    protocol = 'air_temp_monthlies'
    data = get_measurements(protocol, country)
    protocol_data_list = data['features']
    for protocol_data in protocol_data_list:
        new_data = {
            'airtempmonthliesAverageTempC': protocol_data['properties']['airtempmonthliesAverageTempC'],
            'airtempmonthliesAveragedMonth': protocol_data['properties']['airtempmonthliesAveragedMonth'],
            'airtempmonthliesMaximumTempC': protocol_data['properties']['airtempmonthliesMaximumTempC'],
            'airtempmonthliesMinimumTempC': protocol_data['properties']['airtempmonthliesMinimumTempC'],
            'airtempmonthliesNumberOfDaysReported': protocol_data['properties']['airtempmonthliesNumberOfDaysReported'],
            'airtempmonthliesNumberOfObs': protocol_data['properties']['airtempmonthliesNumberOfObs'],
            'date': protocol_data['properties']['airtempmonthliesAveragedMonth'],
            'protocol': protocol,
            'country_name': protocol_data['properties']['countryName'],
            'site_name': protocol_data['properties']['siteName'],
            'site_id': protocol_data['properties']['siteId'],
            'elevation': protocol_data['properties']['elevation'],
            'geometry': protocol_data['geometry'],
        }
        air_temp_monthlies_data.append(new_data)

    air_temp_monthlies_df = GeoDataFrame(air_temp_monthlies_data)
    if air_temp_monthlies_df.empty:
        return air_temp_monthlies_df

    df = pd.DataFrame(air_temp_monthlies_data)
    print(df)
    df['geometry'] = df['geometry'].apply(lambda x: Point(x['coordinates']))
    air_temp_monthlies_df = GeoDataFrame(df, crs='EPSG:4326', geometry=df['geometry'])

    return air_temp_monthlies_df


def get_humidity_monthlies_data(country: str):
    print('get_humidity_monthlies')
    humidity_monthlies_data = []

    protocol = 'humidity_monthlies'
    data = get_measurements(protocol, country)
    protocol_data_list = data['features']
    for protocol_data in protocol_data_list:
        new_data = {
            'humiditymonthliesAverageDewpointC': protocol_data['properties']['humiditymonthliesAverageDewpointC'],
            'humiditymonthliesAverageRelativeHumidityPercent': protocol_data['properties']['humiditymonthliesAverageRelativeHumidityPercent'],
            'humiditymonthliesAveragedMonth': protocol_data['properties']['humiditymonthliesAveragedMonth'],
            'humiditymonthliesMaxRelativeHumidityPercent': protocol_data['properties']['humiditymonthliesMaxRelativeHumidityPercent'],
            'humiditymonthliesMaximumDewpointC': protocol_data['properties']['humiditymonthliesMaximumDewpointC'],
            'humiditymonthliesMinRelativeHumidityPercent': protocol_data['properties']['humiditymonthliesMinRelativeHumidityPercent'],
            'humiditymonthliesMinimumDewpointC': protocol_data['properties']['humiditymonthliesMinimumDewpointC'],
            'humiditymonthliesNumberOfDaysReported': protocol_data['properties']['humiditymonthliesNumberOfDaysReported'],
            'humiditymonthliesNumberOfObs': protocol_data['properties']['humiditymonthliesNumberOfObs'],
            'date': protocol_data['properties']['humiditymonthliesAveragedMonth'],
            'protocol': protocol,
            'country_name': protocol_data['properties']['countryName'],
            'site_name': protocol_data['properties']['siteName'],
            'site_id': protocol_data['properties']['siteId'],
            'elevation': protocol_data['properties']['elevation'],
            'geometry': protocol_data['geometry'],
        }
        humidity_monthlies_data.append(new_data)

    humidity_monthlies_df = GeoDataFrame(humidity_monthlies_data)
    if humidity_monthlies_df.empty:
        return humidity_monthlies_df

    df = pd.DataFrame(humidity_monthlies_data)
    df['geometry'] = df['geometry'].apply(lambda x: Point(x['coordinates']))
    humidity_monthlies_df = GeoDataFrame(df, crs='EPSG:4326', geometry=df['geometry'])

    return humidity_monthlies_df


def run_all_data(country: str):
    precipitation_monthlies_df = get_precipitation_monthlies_data(country)
    soil_characterizations_df = get_soil_characterizations_data(country)
    soil_phs_df = get_soil_phs_data(country)
    soil_fertilities_df = get_soil_fertilities_data(country)
    soil_moisture_for_smap_df = get_soil_moisture_for_smap_data(country)
    soil_moisture_via_gravimetrics_df = get_soil_moisture_via_gravimetrics_data(country)
    air_temp_monthlies_df = get_air_temp_monthlies_data(country)
    humidity_monthlies_df = get_humidity_monthlies_data(country)

    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
    with engine.connect() as conn:
        if not precipitation_monthlies_df.empty:
            precipitation_monthlies_df.to_postgis(
                name='precipitation_monthlies',
                con=conn,
                if_exists='append',
                index=False,
                dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)},
            )
        if not soil_characterizations_df.empty:
            soil_characterizations_df.to_postgis(
                name='soil_characterizations',
                con=conn,
                if_exists='append',
                index=False,
                dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)},
            )
        if not soil_phs_df.empty:
            soil_phs_df.to_postgis(
                name='soil_phs',
                con=conn,
                if_exists='append',
                index=False,
                dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)},
            )
        if not soil_fertilities_df.empty:
            soil_fertilities_df.to_postgis(
                name='soil_fertilities',
                con=conn,
                if_exists='append',
                index=False,
                dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)},
            )
        if not soil_moisture_for_smap_df.empty:
            soil_moisture_for_smap_df.to_postgis(
                name='soil_moisture_for_smap',
                con=conn,
                if_exists='append',
                index=False,
                dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)},
            )
        if not soil_moisture_via_gravimetrics_df.empty:
            soil_moisture_via_gravimetrics_df.to_postgis(
                name='soil_moisture_via_gravimetrics',
                con=conn,
                if_exists='append',
                index=False,
                dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)},
            )
        if not air_temp_monthlies_df.empty:
            air_temp_monthlies_df.to_postgis(
                name='air_temp_monthlies',
                con=conn,
                if_exists='append',
                index=False,
                dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)},
            )
        if not humidity_monthlies_df.empty:
            humidity_monthlies_df.to_postgis(
                name='humidity_monthlies',
                con=conn,
                if_exists='append',
                index=False,
                dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)},
            )


if __name__ == '__main__':
    COUNTRY_CODES = ['PRI', 'PRK', 'PRT', 'PRY', 'PSE', 'PYF', 'QAT', 'ROU', 'RUS', 'RWA', 'SAU', 'SDN', 'SEN', 'SGP', 'SGS', 'SHN', 'SLB', 'SLE', 'SLV', 'SMR', 'SOM', 'SPM', 'SRB', 'SSD', 'STP', 'SUR', 'SVK', 'SVN', 'SWE', 'SWZ', 'SXM', 'SYC', 'SYR', 'TCA', 'TCD', 'TGO', 'THA', 'TJK', 'TKM', 'TLS', 'TON', 'TTO', 'TUN', 'TUR', 'TUV', 'TWN', 'TZA', 'UGA', 'UKR', 'UMI', 'URY', 'USA', 'UZB', 'VAT', 'VCT', 'VEN', 'VGB', 'VIR', 'VNM', 'VUT', 'WLF', 'WSM', 'YEM', 'ZAF', 'ZMB', 'ZWE']

    for country in COUNTRY_CODES:
        run_all_data(country)
