from .enums import EconomicCrops, AnalyzerTypes


def to_float(value):
    try:
        return float(value)
    except:
        return None


class EnvironmentParameter:
    def __init__(self, site_dict: dict):
        self.site_id = site_dict["site_id"]
        self.site_name = site_dict["site_name"]
        self.date = site_dict["date"]
        self.geometry = site_dict["geometry"]
        self.airtempmonthliesNumberOfObs = site_dict["airtempmonthliesNumberOfObs"]
        self.airtempmonthliesAverageTempC = site_dict["airtempmonthliesAverageTempC"]
        self.airtempmonthliesMaximumTempC = site_dict["airtempmonthliesMaximumTempC"]
        self.airtempmonthliesMinimumTempC = site_dict["airtempmonthliesMinimumTempC"]
        self.airtempmonthliesAveragedMonth = site_dict["airtempmonthliesAveragedMonth"]
        self.humiditymonthliesNumberOfObs = site_dict["humiditymonthliesNumberOfObs"]
        self.humiditymonthliesAveragedMonth = site_dict[
            "humiditymonthliesAveragedMonth"
        ]
        self.humiditymonthliesAverageDewpointC = site_dict[
            "humiditymonthliesAverageDewpointC"
        ]
        self.humiditymonthliesMaximumDewpointC = site_dict[
            "humiditymonthliesMaximumDewpointC"
        ]
        self.humiditymonthliesMinimumDewpointC = site_dict[
            "humiditymonthliesMinimumDewpointC"
        ]
        self.humiditymonthliesNumberOfDaysReported = site_dict[
            "humiditymonthliesNumberOfDaysReported"
        ]
        self.humiditymonthliesMaxRelativeHumidityPercent = site_dict[
            "humiditymonthliesMaxRelativeHumidityPercent"
        ]
        self.humiditymonthliesMinRelativeHumidityPercent = site_dict[
            "humiditymonthliesMinRelativeHumidityPercent"
        ]
        self.humiditymonthliesAverageRelativeHumidityPercent = site_dict[
            "humiditymonthliesAverageRelativeHumidityPercent"
        ]
        self.precipitationmonthliesLiquidAccumulationMm = site_dict[
            "precipitationmonthliesLiquidAccumulationMm"
        ]
        self.soilmoistureforsmapComments = site_dict["soilmoistureforsmapComments"]
        self.soilmoistureforsmapSoilState = site_dict["soilmoistureforsmapSoilState"]
        self.soilmoistureforsmapDepthLevelCm = site_dict[
            "soilmoistureforsmapDepthLevelCm"
        ]
        self.soilmoistureforsmapSaturatedFlag = site_dict[
            "soilmoistureforsmapSaturatedFlag"
        ]
        self.soilmoistureviagravimetricsSoilState = site_dict[
            "soilmoistureviagravimetricsSoilState"
        ]
        self.soilmoistureviagravimetricsDepthLevelCm = site_dict[
            "soilmoistureviagravimetricsDepthLevelCm"
        ]
        self.soilmoistureforsmapAverageSampleVolumeMl = site_dict[
            "soilmoistureforsmapAverageSampleVolumeMl"
        ]
        self.soilmoistureviagravimetricsSaturatedFlag = site_dict[
            "soilmoistureviagravimetricsSaturatedFlag"
        ]
        self.soilmoistureforsmapFirstVolumeMeasurement = site_dict[
            "soilmoistureforsmapFirstVolumeMeasurement"
        ]
        self.soilmoistureviagravimetricsMoistureMethod = site_dict[
            "soilmoistureviagravimetricsMoistureMethod"
        ]
        self.soilmoistureforsmapSampleBulkDensityGPerMl = site_dict[
            "soilmoistureforsmapSampleBulkDensityGPerMl"
        ]

    @staticmethod
    def from_site_dict(site_dict: dict) -> "EnvironmentParameter":
        return EnvironmentParameter(site_dict)

    def __str__(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "site_id": self.site_id,
            "site_name": self.site_name,
            "date": self.date,
            "geometry": self.geometry,
            "airtempmonthliesNumberOfObs": to_float(self.airtempmonthliesNumberOfObs),
            "airtempmonthliesAverageTempC": to_float(self.airtempmonthliesAverageTempC),
            "airtempmonthliesMaximumTempC": to_float(self.airtempmonthliesMaximumTempC),
            "airtempmonthliesMinimumTempC": to_float(self.airtempmonthliesMinimumTempC),
            "airtempmonthliesAveragedMonth": self.airtempmonthliesAveragedMonth,
            "humiditymonthliesNumberOfObs": to_float(self.humiditymonthliesNumberOfObs),
            "humiditymonthliesAveragedMonth": self.humiditymonthliesAveragedMonth,
            "humiditymonthliesAverageDewpointC": to_float(
                self.humiditymonthliesAverageDewpointC
            ),
            "humiditymonthliesMaximumDewpointC": to_float(
                self.humiditymonthliesMaximumDewpointC
            ),
            "humiditymonthliesMinimumDewpointC": to_float(
                self.humiditymonthliesMinimumDewpointC
            ),
            "humiditymonthliesNumberOfDaysReported": to_float(
                self.humiditymonthliesNumberOfDaysReported
            ),
            "humiditymonthliesMaxRelativeHumidityPercent": to_float(
                self.humiditymonthliesMaxRelativeHumidityPercent
            ),
            "humiditymonthliesMinRelativeHumidityPercent": to_float(
                self.humiditymonthliesMinRelativeHumidityPercent
            ),
            "humiditymonthliesAverageRelativeHumidityPercent": to_float(
                self.humiditymonthliesAverageRelativeHumidityPercent
            ),
            "precipitationmonthliesLiquidAccumulationMm": to_float(
                self.precipitationmonthliesLiquidAccumulationMm
            ),
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

    def to_readable_dict(self) -> dict:
        dict_ = {
            "Site Name": self.site_name,
        }

        if self.airtempmonthliesAverageTempC:
            dict_["Average Temperature"] = self.airtempmonthliesAverageTempC

        if self.humiditymonthliesAverageRelativeHumidityPercent:
            dict_["Average Humidity"] = (
                self.humiditymonthliesAverageRelativeHumidityPercent
            )

        if self.precipitationmonthliesLiquidAccumulationMm:
            dict_["Precipitation Liquid Accumulation (mm)"] = (
                self.precipitationmonthliesLiquidAccumulationMm
            )

        if self.soilmoistureforsmapComments:
            dict_["Soil Moisture Comments"] = self.soilmoistureforsmapComments

        if self.soilmoistureforsmapSoilState:
            dict_["Soil State"] = self.soilmoistureforsmapSoilState

        if self.soilmoistureforsmapSampleBulkDensityGPerMl:
            dict_["Soil Sample Bulk Density (g/ml)"] = (
                self.soilmoistureforsmapSampleBulkDensityGPer
            )

        return dict_


# The suggested crop after analyzing the environment paramters
class SuggestedCrop:
    def __init__(
        self,
        name: EconomicCrops,
        reason: str,
        type_: AnalyzerTypes,
        options: dict = None,
    ):
        self.analyzer_type = type_
        self.name = name
        self.reason = reason
        self.options = options

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "reason": self.reason,
            "analyzer_type": self.analyzer_type.value,
        }
