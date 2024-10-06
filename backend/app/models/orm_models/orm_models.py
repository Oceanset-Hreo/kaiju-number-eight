import geojson
import shapely
import json
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry

from app import db
from app.settings import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)


def ewkb_route_to_coordinates(geometry):
    return geojson.Feature(
        geometry=shapely.wkb.loads(str(geometry), True), properties={}
    )["geometry"]["coordinates"]


class Site(db.Model):
    __tablename__ = "latest_data"

    site_id = mapped_column(db.String, primary_key=True)
    site_name = mapped_column(db.String)
    date = mapped_column(db.Date)
    geometry = mapped_column(Geometry(geometry_type="POINT", srid=4326))
    airtempmonthliesNumberOfObs = mapped_column(db.String)
    airtempmonthliesAverageTempC = mapped_column(db.String)
    airtempmonthliesMaximumTempC = mapped_column(db.String)
    airtempmonthliesMinimumTempC = mapped_column(db.String)
    airtempmonthliesAveragedMonth = mapped_column(db.String)
    humiditymonthliesNumberOfObs = mapped_column(db.String)
    humiditymonthliesAveragedMonth = mapped_column(db.String)
    humiditymonthliesAverageDewpointC = mapped_column(db.String)
    humiditymonthliesMaximumDewpointC = mapped_column(db.String)
    humiditymonthliesMinimumDewpointC = mapped_column(db.String)
    humiditymonthliesNumberOfDaysReported = mapped_column(db.String)
    humiditymonthliesMaxRelativeHumidityPercent = mapped_column(db.String)
    humiditymonthliesMinRelativeHumidityPercent = mapped_column(db.String)
    humiditymonthliesAverageRelativeHumidityPercent = mapped_column(db.String)
    precipitationmonthliesLiquidAccumulationMm = mapped_column(db.String)
    soilmoistureforsmapComments = mapped_column(db.String)
    soilmoistureforsmapSoilState = mapped_column(db.String)
    soilmoistureforsmapDepthLevelCm = mapped_column(db.String)
    soilmoistureforsmapSaturatedFlag = mapped_column(db.String)
    soilmoistureviagravimetricsSoilState = mapped_column(db.String)
    soilmoistureviagravimetricsDepthLevelCm = mapped_column(db.String)
    soilmoistureforsmapAverageSampleVolumeMl = mapped_column(db.String)
    soilmoistureviagravimetricsSaturatedFlag = mapped_column(db.String)
    soilmoistureforsmapFirstVolumeMeasurement = mapped_column(db.String)
    soilmoistureviagravimetricsMoistureMethod = mapped_column(db.String)
    soilmoistureforsmapSampleBulkDensityGPerMl = mapped_column(db.String)

    def to_dict(self):

        return {
            "site_id": self.site_id,
            "site_name": self.site_name,
            "date": self.date,
            "geometry": ewkb_route_to_coordinates(self.geometry),
            "airtempmonthliesNumberOfObs": self.airtempmonthliesNumberOfObs,
            "airtempmonthliesAverageTempC": self.airtempmonthliesAverageTempC,
            "airtempmonthliesMaximumTempC": self.airtempmonthliesMaximumTempC,
            "airtempmonthliesMinimumTempC": self.airtempmonthliesMinimumTempC,
            "airtempmonthliesAveragedMonth": self.airtempmonthliesAveragedMonth,
            "humiditymonthliesNumberOfObs": self.humiditymonthliesNumberOfObs,
            "humiditymonthliesAveragedMonth": self.humiditymonthliesAveragedMonth,
            "humiditymonthliesAverageDewpointC": self.humiditymonthliesAverageDewpointC,
            "humiditymonthliesMaximumDewpointC": self.humiditymonthliesMaximumDewpointC,
            "humiditymonthliesMinimumDewpointC": self.humiditymonthliesMinimumDewpointC,
            "humiditymonthliesNumberOfDaysReported": self.humiditymonthliesNumberOfDaysReported,
            "humiditymonthliesMaxRelativeHumidityPercent": self.humiditymonthliesMaxRelativeHumidityPercent,
            "humiditymonthliesMinRelativeHumidityPercent": self.humiditymonthliesMinRelativeHumidityPercent,
            "humiditymonthliesAverageRelativeHumidityPercent": self.humiditymonthliesAverageRelativeHumidityPercent,
            "precipitationmonthliesLiquidAccumulationMm": self.precipitationmonthliesLiquidAccumulationMm,
            "soilmoistureforsmapComments": self.soilmoistureforsmapComments,
            "soilmoistureforsmapSoilState": self.soilmoistureforsmapSoilState,
            "soilmoistureforsmapDepthLevelCm": self.soilmoistureforsmapDepthLevelCm,
            "soilmoistureforsmapSaturatedFlag": self.soilmoistureforsmapSaturatedFlag,
            "soilmoistureviagravimetricsSoilState": self.soilmoistureviagravimetricsSoilState,
            "soilmoistureviagravimetricsDepthLevelCm": self.soilmoistureviagravimetricsDepthLevelCm,
            "soilmoistureforsmapAverageSampleVolumeMl": self.soilmoistureforsmapAverageSampleVolumeMl,
            "soilmoistureviagravimetricsSaturatedFlag": self.soilmoistureviagravimetricsSaturatedFlag,
            "soilmoistureforsmapFirstVolumeMeasurement": self.soilmoistureforsmapFirstVolumeMeasurement,
            "soilmoistureviagravimetricsMoistureMethod": self.soilmoistureviagravimetricsMoistureMethod,
            "soilmoistureforsmapSampleBulkDensityGPerMl": self.soilmoistureforsmapSampleBulkDensityGPerMl,
        }


class SiteInfo(db.Model):
    __tablename__ = "site_info"

    site_id = mapped_column(db.String, primary_key=True)
    site_name = mapped_column(db.String)
    geometry = mapped_column(Geometry(geometry_type="POINT", srid=4326))

    def to_dict(self):
        print(self.geometry)
        return {
            "site_id": self.site_id,
            "site_name": self.site_name,
            "geometry": ewkb_route_to_coordinates(self.geometry),
        }


class SuitableCrop(db.Model):
    __tablename__ = "production_data"

    ADMIN1_NAME = mapped_column(db.String)
    geometry = mapped_column(
        Geometry(geometry_type="POINT", srid=4326), primary_key=True
    )
    ADM1 = mapped_column(db.Integer)
    CTR = mapped_column(db.String)
    CRP = mapped_column(db.String)
    EXTENTS = mapped_column(db.Float)
    SUIT_VS = mapped_column(db.Float)
    SUIT_S = mapped_column(db.Float)
    SUIT_MS = mapped_column(db.Float)
    SUIT_mS = mapped_column(db.Float)
    SUIT_vmS = mapped_column(db.Float)
    SUIT_NS = mapped_column(db.Float)
    PROD_VS = mapped_column(db.Float)
    PROD_S = mapped_column(db.Float)
    PROD_MS = mapped_column(db.Float)
    PROD_mS = mapped_column(db.Float)
    PROD_vmS = mapped_column(db.Float)
    # How many percentage of the area is very suitable for the crop
    A_level = mapped_column(db.Float)
    # # How many percentage of the area is very suitable and suitable for the crop
    B_level = mapped_column(db.Float)
    C_level = mapped_column(db.Float)
    D_level = mapped_column(db.Float)
    E_level = mapped_column(db.Float)

    def to_dict(self) -> dict:
        return {
            "crop": self.CRP,
            "total_area": self.EXTENTS,
            "suitable_area_percentage": self.C_level,
            "name": self.ADMIN1_NAME,
            "geometry": ewkb_route_to_coordinates(self.geometry),
        }
