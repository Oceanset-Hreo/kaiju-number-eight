import json
from typing import List
from abc import abstractmethod

from app.models.ai import get_ai_response
from app.models.orm_models import get_sutibale_crops
from app.utils import km_to_degree

from .models import EnvironmentParameter, SuggestedCrop
from .enums import AnalyzerTypes, EconomicCrops
from .constants import CROPS_ANALYZE_PROMPT, CROPS, SEARCH_SUTIABLE_CROPS_DISTANCE


class BaseAnalyzer:

    @abstractmethod
    def analyze(
        self, parameter: EnvironmentParameter, location: str
    ) -> List[SuggestedCrop]:
        raise NotImplementedError("Analyze method is not implemented")


class AIAnalyzer(BaseAnalyzer):

    def _parse_response(self, response: str) -> List[SuggestedCrop]:
        crops = json.loads(response)

        return [
            SuggestedCrop(
                name=crop["crop"], reason=crop["reason"], type_=AnalyzerTypes.AI
            )
            for crop in crops
        ]

    def _build_prompt(self, parameter: EnvironmentParameter, location: str) -> str:
        parameter_dict = parameter.to_readable_dict()
        parameter_dict["Location"] = location
        parameter_prompt = "\n".join(
            [f" - {k}: {v}" for k, v in parameter_dict.items()]
        )

        return CROPS_ANALYZE_PROMPT.format(
            parameter_prompt=parameter_prompt, crops=CROPS
        )

    def analyze(
        self, parameter: EnvironmentParameter, location: str
    ) -> List[SuggestedCrop]:

        prompt = self._build_prompt(parameter, location)
        print(prompt)

        try:
            response = get_ai_response(prompt)
            suggested_crops = self._parse_response(response)
        except Exception as e:
            print("Error occurred while analyzing", e)
            suggested_crops = []

        return suggested_crops


class RuleBasedAnalyzer(BaseAnalyzer):

    def _check_wheat(self, parameter_dict: dict) -> bool:
        """
        Check if wheat can be grown in the given environment
        https://s3.eu-west-1.amazonaws.com/data.gaezdev.aws.fao.org/crop_profiles/GAEZ_Crop_profile_wheat.pdf
        """

        # Optimal temperature range for wheat is 15°C to 20°C, with growth still possible down to 5°C and up to 30°C
        if not (
            parameter_dict["airtempmonthliesAverageTempC"] is not None
            and parameter_dict["airtempmonthliesAverageTempC"] >= 5
            and parameter_dict["airtempmonthliesAverageTempC"] <= 30
        ):
            return None

        # Wheat requires adequate moisture, but the exact requirement can vary. We assume a minimum needed.
        if not (
            parameter_dict["precipitationmonthliesLiquidAccumulationMm"] is not None
            and parameter_dict["precipitationmonthliesLiquidAccumulationMm"] > 50
            and parameter_dict["precipitationmonthliesLiquidAccumulationMm"] < 150
        ):
            return None

        return SuggestedCrop(
            name=EconomicCrops.WHEAT.value,
            reason="The precipitation and temperature are suitable for wheat",
            type_=AnalyzerTypes.RULE_BASED,
        )

    def _check_maize(self, parameter_dict: dict) -> bool:
        """
        Check if maize can be grown in the given environment
        https://s3.eu-west-1.amazonaws.com/data.gaezdev.aws.fao.org/crop_profiles/GAEZ_Crop_profile_maize.pdf
        """

        # Optimal temperature range for maize is 20°C to 30°C
        if not (
            parameter_dict["airtempmonthliesAverageTempC"] is not None
            and parameter_dict["airtempmonthliesAverageTempC"] >= 10
            and parameter_dict["airtempmonthliesAverageTempC"] <= 30
            # Temperatures above 40°C may cause heat stress
            and parameter_dict["airtempmonthliesMaximumTempC"] is not None
            and parameter_dict["airtempmonthliesMaximumTempC"] <= 40
        ):
            return None

        # Maize requires adequate moisture, but the exact requirement can vary. We assume a minimum needed.
        if not (
            parameter_dict["precipitationmonthliesLiquidAccumulationMm"] is not None
            and parameter_dict["precipitationmonthliesLiquidAccumulationMm"] > 50
            and parameter_dict["precipitationmonthliesLiquidAccumulationMm"] < 150
        ):
            return None

        return SuggestedCrop(
            name=EconomicCrops.MAIZE.value,
            reason="The precipitation and temperature are suitable for maize",
            type_=AnalyzerTypes.RULE_BASED,
        )

    def analyze(
        self, parameter: EnvironmentParameter, location: str
    ) -> List[SuggestedCrop]:

        parameter_dict = parameter.to_dict()

        return [
            suggested_crop
            for suggested_crop in [
                self._check_wheat(parameter_dict),
                self._check_maize(parameter_dict),
            ]
            if suggested_crop is not None
        ]


class StatisticsAnalyzer(BaseAnalyzer):

    def analyze(
        self, parameter: EnvironmentParameter, location: str
    ) -> List[SuggestedCrop]:

        parameter_dict = parameter.to_dict()
        longitude = parameter_dict["geometry"][0]
        lantitude = parameter_dict["geometry"][1]

        sutibale_crops = get_sutibale_crops(longitude, lantitude, km_to_degree(SEARCH_SUTIABLE_CROPS_DISTANCE))
        print(sutibale_crops)
        crop_dicts = [crop.to_dict() for crop in sutibale_crops]

        print("crop_dicts", crop_dicts)

        return [
            SuggestedCrop(
                name=crop_dict["crop"],
                reason=f"The surrounding area of {crop_dict["total_area"]} km² has {int(crop_dict["suitable_area_percentage"] * 100) / 100}% of its land classified as suitable for wheat cultivation.",
                type_=AnalyzerTypes.STATISTICS,
                options={
                    "total_area": crop_dict["total_area"],
                    "suitable_area_percentage": crop_dict["suitable_area_percentage"],
                }
            )
            for crop_dict in crop_dicts
        ]
