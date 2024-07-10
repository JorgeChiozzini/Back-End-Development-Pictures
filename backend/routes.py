from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    return {"message": "picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    if not request.json or "id" not in request.json:
        abort(400)

    new_picture = {
        "id": request.json["id"],
        "pic_url": request.json.get("pic_url", ""),
        "event_country": request.json.get("event_country", ""),
        "event_state": request.json.get("event_state", ""),
        "event_city": request.json.get("event_city", ""),
        "event_date": request.json.get("event_date", "")
    }

    existing_picture = next((item for item in data if item["id"] == new_picture["id"]), None)
    if existing_picture:
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    data.append(new_picture)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return jsonify({"message": "picture not found"}), 404

    if not request.json:
        abort(400)

    picture.update({
        "pic_url": request.json.get("pic_url", picture["pic_url"]),
        "event_country": request.json.get("event_country", picture["event_country"]),
        "event_state": request.json.get("event_state", picture["event_state"]),
        "event_city": request.json.get("event_city", picture["event_city"]),
        "event_date": request.json.get("event_date", picture["event_date"])
    })
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return jsonify({"message": "picture not found"}), 404

    data = [item for item in data if item["id"] != id]
    return '', 204
