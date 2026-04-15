import uuid

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound, UnprocessableEntity

from models import tasks


tasks_bp = Blueprint("tasks", __name__)


def _find_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise NotFound(f"Task '{task_id}' was not found.")


def _require_json_body():
    data = request.get_json(silent=True)
    if data is None:
        raise BadRequest("Request body must be valid JSON.")
    if not isinstance(data, dict):
        raise BadRequest("Request body must be a JSON object.")
    return data


def _validate_title(value):
    if not isinstance(value, str):
        raise BadRequest("title must be a string.")
    cleaned_title = value.strip()
    if not cleaned_title:
        raise UnprocessableEntity("title must contain text.")
    return cleaned_title


def _validate_completed(value):
    if not isinstance(value, bool):
        raise BadRequest("completed must be a boolean.")
    return value


@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({
        "success": True,
        "data": tasks,
    })


@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = _find_task(task_id)
    return jsonify({
        "success": True,
        "data": task,
    })


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = _require_json_body()

    if "title" not in data:
        raise BadRequest("title is required.")

    new_task = {
        "id": str(uuid.uuid4()),
        "title": _validate_title(data["title"]),
        "completed": False,
    }

    tasks.append(new_task)
    return jsonify({
        "success": True,
        "data": new_task,
    }), 201


@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def change_task(task_id):
    data = _require_json_body()
    if not data:
        raise BadRequest("Update request must include at least one field.")

    allowed_fields = {"title", "completed"}
    invalid_fields = sorted(set(data) - allowed_fields)
    if invalid_fields:
        raise BadRequest(
            f"Unsupported field(s): {', '.join(invalid_fields)}."
        )

    task = _find_task(task_id)

    if "title" in data:
        task["title"] = _validate_title(data["title"])
    if "completed" in data:
        task["completed"] = _validate_completed(data["completed"])

    return jsonify({
        "success": True,
        "data": task,
    })


@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = _find_task(task_id)
    tasks.remove(task)

    return jsonify({
        "success": True,
        "message": f"Removed task '{task['title']}'.",
    })
