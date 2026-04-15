from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity
from models import tasks
import uuid


tasks_bp = Blueprint("tasks",__name__)

# create route for getting all tasks
@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    return tasks

# route for getting task by id
@tasks_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task_id == task["id"]:
             return task
    raise NotFound(f"{task_id} not found")  

# create a task
@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data:
        raise BadRequest("request body must be json")
    title = data["title"]
    if not isinstance(title, str):
        raise BadRequest("title must be a string")
    if not title.strip():
        raise UnprocessableEntity("title must contain text")
    new_task = {
    "id": str(uuid.uuid4()),
    "title": title.strip(),
    "completed": False
        }
    tasks.append(new_task)
    return jsonify({
        "success": True,
        "data": new_task
    }), 201
        
# update a task
@tasks_bp.route("/tasks/<task_id>", methods=["PUT"])
def change_task(task_id):
    data = request.get_json()
    if not data:
        raise BadRequest("error: update request must contain data")
    keys = ("title", "completed")
    for key in data.keys():
        if key not in keys:
            raise BadRequest(f"not allowed to pass {key}")
    for task in tasks:
            if task_id == task["id"]:
                if "title" in data:
                    task["title"] = data["title"]
                if "completed" in data:
                    task["completed"] = data["completed"]
                return task
    raise NotFound(f"{task_id} not found")
    
# delete function route
@tasks_bp.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            
            return {
                "Message": f"removed task {task['title']}"
            }
    raise NotFound(f"{task_id} not found")