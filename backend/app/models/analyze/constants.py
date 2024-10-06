from .enums import EconomicCrops

CROPS = values = [member.value for member in EconomicCrops.__members__.values()]

CROPS_ANALYZE_PROMPT = """Based on the following environment parameters and location:
{parameter_prompt}

And the available eco crops:
{crops}

Please return a **pure JSON** object without any code block formatting, markdown, or additional symbols.

The JSON is n array that includes only the crops from the provided list that are suitable for the given parameters, along with a `reason` field explaining why each crop is suitable.

Make sure the output is plain text and starts directly with the JSON object, containing only the suggested crops."""


CROP_PLANTING_ADVICE_PROMPT = """Based on the following environment parameters and location:
{parameter_prompt}

And the selected crop:
{crop}

Please give some advice on how to plant the selected crop in the given location.
Please keep the output concise, not exceeding two sentences
"""


SEARCH_SUTIABLE_CROPS_DISTANCE = 10000
