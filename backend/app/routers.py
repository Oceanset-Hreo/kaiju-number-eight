from flask import jsonify, request

from app.utils import km_to_degree

from app.models.analyze.models import EnvironmentParameter
from app.models.analyze import analyze as _analyze, advice as _advice
from app.models.orm_models import get_site, get_sites, get_sutibale_crops
from . import app


@app.route("/api/", methods=["GET"])
def home():
    return jsonify(message="Hello, API")


@app.route("/api/test", methods=["GET"])
def test():
    site = get_site("102436")

    return jsonify(site.to_dict())


@app.route("/api/list", methods=["GET"])
def list_():
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))

    # unit: km
    distance = float(request.args.get("distance", 100))

    # 1 degree = 111.32km
    distance_degree = km_to_degree(distance)
    site_infos = get_sites(latitude, longitude, distance_degree)

    return jsonify([site_info.to_dict() for site_info in site_infos])


@app.route("/api/describe/<string:site_id>", methods=["GET"])
def describe(site_id: str):
    location = request.args.get("location")
    site = get_site(site_id)
    site_dict = site.to_dict()
    environment_params = EnvironmentParameter.from_site_dict(site_dict)
    suggest_crops = _analyze(environment_params, location)

    return_suggest_crops = []
    reason_crops = []
    for suggest_crop in suggest_crops:
        suggest_crop_json = suggest_crop.to_dict()
        reason_crop = {
            "name": suggest_crop_json['name'],
            "analyzer_type": suggest_crop_json['analyzer_type']
        }
        if reason_crop in reason_crops:
            continue
        return_suggest_crops.append(suggest_crop_json)
        reason_crops.append(reason_crop)

    return jsonify(
        {
            "site": site_dict,
            "suggest_crops": return_suggest_crops,
        }
    )


@app.route("/api/advice/<string:site_id>", methods=["GET"])
def advice(site_id: str):

    location = request.args.get("location")
    crop = request.args.get("crop")

    site = get_site(site_id)
    site_dict = site.to_dict()
    environment_params = EnvironmentParameter.from_site_dict(site_dict)

    suggestion = _advice(crop, environment_params, location)

    return jsonify({"suggestion": suggestion})


@app.route("/api/search", methods=["GET"])
def search():
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))

    # unit: km
    distance = float(request.args.get("distance", 100))
    crop = request.args.get("crop")

    sutiable_crops = get_sutibale_crops(latitude, longitude, km_to_degree(distance), crop)

    return jsonify([crop.to_dict() for crop in sutiable_crops])
