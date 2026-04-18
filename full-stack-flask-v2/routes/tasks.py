from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity

from models.list import get_list_by_id
from models.task import get_tasks_for_list, get_task_by_id, create_task, update_task, delete_task

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/lists/<list_id>/tasks", methods=["GET"])
def get_tasks(list_id):
    if not get_list_by_id(list_id):
        raise NotFound(f"list {list_id} not found")
    return jsonify(get_tasks_for_list(list_id))


@tasks_bp.route("/lists/<list_id>/tasks", methods=["POST"])
def create_task_route(list_id):
    if not get_list_by_id(list_id):
        raise NotFound(f"list {list_id} not found")
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise BadRequest("request body must be json")
    if "title" not in data:
        raise BadRequest("title is required")
    title = data["title"]
    if not isinstance(title, str):
        raise BadRequest("title must be a string")
    if not title.strip():
        raise UnprocessableEntity("title must contain text")
    new_task = create_task(list_id, title.strip())
    return jsonify({"success": True, "data": new_task}), 201


@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        raise NotFound(f"{task_id} not found")
    task["_id"] = str(task["_id"])
    return jsonify(task)


@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def change_task(task_id):
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise BadRequest("request body must contain data")
    allowed = ("title", "completed")
    for key in data:
        if key not in allowed:
            raise BadRequest(f"not allowed to pass {key}")

    update = {}
    if "title" in data:
        if not isinstance(data["title"], str):
            raise BadRequest("title must be a string")
        if not data["title"].strip():
            raise UnprocessableEntity("title must contain text")
        update["title"] = data["title"].strip()
    if "completed" in data:
        if not isinstance(data["completed"], bool):
            raise BadRequest("completed must be a boolean")
        update["completed"] = data["completed"]

    result = update_task(task_id, update)
    if not result:
        raise NotFound(f"{task_id} not found")
    result["_id"] = str(result["_id"])
    return jsonify(result)


@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task_route(task_id):
    task = delete_task(task_id)
    if not task:
        raise NotFound(f"{task_id} not found")
    return jsonify({"message": f"removed task {task['title']}"})
