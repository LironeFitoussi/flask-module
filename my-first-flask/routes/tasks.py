from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity
from bson import ObjectId
from bson.errors import InvalidId
from db import get_collection

tasks_bp = Blueprint("tasks", __name__)

def serialize(task):
    task["_id"] = str(task["_id"])
    return task


@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    col = get_collection("todo")
    tasks = list(col.find())
    return jsonify({"success": True, "data": [serialize(t) for t in tasks]})


@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    col = get_collection("todo")
    try:
        task = col.find_one({"_id": ObjectId(task_id)})
    except InvalidId:
        raise BadRequest("invalid task id")
    if not task:
        raise NotFound(f"{task_id} not found")
    return jsonify({"success": True, "data": serialize(task)})


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
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

    new_task = {"title": title.strip(), "completed": False}
    col = get_collection("todo")
    col.insert_one(new_task)
    return jsonify({"success": True, "data": serialize(new_task)}), 201


@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def change_task(task_id):
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        raise BadRequest("error: update request must contain data")
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

    try:
        col = get_collection("todo")
        task = col.find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": update},
            return_document=True
        )
    except InvalidId:
        raise BadRequest("invalid task id")
    if not task:
        raise NotFound(f"{task_id} not found")
    return jsonify({"success": True, "data": serialize(task)})


@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        col = get_collection("todo")
        task = col.find_one_and_delete({"_id": ObjectId(task_id)})
    except InvalidId:
        raise BadRequest("invalid task id")
    if not task:
        raise NotFound(f"{task_id} not found")
    return jsonify({"success": True, "message": f"removed task {task['title']}"})
