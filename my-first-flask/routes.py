from flask import jsonify, request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest
from models import get_all_tasks, get_task_by_id, create_task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(get_all_tasks())

@tasks_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        raise NotFound(f"Task with ID {task_id} not found")
    return jsonify(task)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task_route():
    if not request.is_json:
        raise BadRequest("Request body must be JSON")
    
    data = request.get_json()
    
    if not data["title"].strip():
        raise BadRequest("title mustnot be empty")
    
    if 'title' not in data:
        raise BadRequest("Missing required field: 'title'")

    new_task = create_task(data)
    return jsonify(new_task), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise NotFound(f"Cannot update: Task {task_id} not found")

    if not request.is_json:
        raise BadRequest("Request body must be JSON")

    data = request.get_json()
    task['title'] = data.get('title', task['title'])
    task['completed'] = data.get('completed', task['completed'])
    
    return jsonify(task)

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise NotFound(f"Cannot delete: Task {task_id} not found")
    
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted successfully"}), 200
