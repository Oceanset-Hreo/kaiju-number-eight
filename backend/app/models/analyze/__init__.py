from typing import List
import itertools

from app.models.ai import get_ai_response

from .constants import CROP_PLANTING_ADVICE_PROMPT
from .analyzers import AIAnalyzer, RuleBasedAnalyzer, StatisticsAnalyzer
from .models import EnvironmentParameter, SuggestedCrop
from .enums import EconomicCrops

# ANALYZERS = [AIAnalyzer, RuleBasedAnalyzer, StatisticsAnalyzer]

ANALYZERS = [StatisticsAnalyzer]


def analyze(environment_params: EnvironmentParameter, location) -> List[SuggestedCrop]:
    analyzers = [analyzer_constructor() for analyzer_constructor in ANALYZERS]
    suggested_crops_lists = [
        analyzer.analyze(environment_params, location) for analyzer in analyzers
    ]
    suggested_crops = list(itertools.chain(*suggested_crops_lists))

    return suggested_crops


def advice(crop: EconomicCrops, environment_params, location) -> str:
    prompt = _build_advice_prompt(crop, environment_params, location)
    print(prompt)
    advice_text = get_ai_response(prompt, temperature=0.3)

    return advice_text


def _build_advice_prompt(
    crop: EconomicCrops, parameter: EnvironmentParameter, location: str
) -> str:
    parameter_dict = parameter.to_readable_dict()
    parameter_dict["location"] = location
    parameter_prompt = "\n".join([f" - {k}: {v}" for k, v in parameter_dict.items()])

    return CROP_PLANTING_ADVICE_PROMPT.format(
        parameter_prompt=parameter_prompt, crop=crop
    )
