from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity

from models.list import get_all_lists, get_list_by_id, create_list, update_list, delete_list

lists_bp = Blueprint("lists", __name__)


@lists_bp.route("/lists", methods=["GET"])
def get_lists():
    return jsonify(get_all_lists())


@lists_bp.route("/lists/<list_id>", methods=["GET"])
def get_list(list_id):
    lst = get_list_by_id(list_id)
    if not lst:
        raise NotFound(f"{list_id} not found")
    lst["_id"] = str(lst["_id"])
    return jsonify(lst)


@lists_bp.route("/lists", methods=["POST"])
def create_list_route():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise BadRequest("request body must be json")
    if "name" not in data:
        raise BadRequest("name is required")
    name = data["name"]
    if not isinstance(name, str):
        raise BadRequest("name must be a string")
    if not name.strip():
        raise UnprocessableEntity("name must contain text")
    new_list = create_list(name.strip())
    return jsonify({"success": True, "data": new_list}), 201


@lists_bp.route("/lists/<list_id>", methods=["PUT"])
def update_list_route(list_id):
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise BadRequest("request body must be json")
    if "name" not in data:
        raise BadRequest("name is required")
    name = data["name"]
    if not isinstance(name, str):
        raise BadRequest("name must be a string")
    if not name.strip():
        raise UnprocessableEntity("name must contain text")
    result = update_list(list_id, name.strip())
    if not result:
        raise NotFound(f"{list_id} not found")
    result["_id"] = str(result["_id"])
    return jsonify(result)


@lists_bp.route("/lists/<list_id>", methods=["DELETE"])
def delete_list_route(list_id):
    lst = delete_list(list_id)
    if not lst:
        raise NotFound(f"{list_id} not found")
    return jsonify({"message": f"removed list {lst['name']}"})
