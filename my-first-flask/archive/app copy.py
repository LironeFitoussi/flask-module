from flask import Flask, request, jsonify
from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity
import uuid

app = Flask(__name__)

todos = [{
    "id": 1,
    "title": "go to the gym",
    "is_completed": True
}]

# next_id = 1

# def get_todo_or_raise(todo_id):
#     for todo in todos:
#         if todo["id"] == todo_id:
#             return todo
    # raise KeyError(f"Todo with id {todo_id} not found")


@app.errorhandler(NotFound)
def handle_type_error(e):
    return jsonify({
        "error": str(e)
    }), 404

@app.errorhandler(BadRequest)
def handle_type_error(e):
    return jsonify({
        "error": str(e)
    }), 400
    
@app.errorhandler(UnprocessableEntity)
def handle_type_error(e):
    return jsonify({
        "error": str(e)
    }), 422
    
@app.route("/todo", methods=["GET"])
def get_todos():
    return jsonify(todos)
    
@app.route("/todo",  methods=["POST"])
def create_todo():
    data = request.get_json()
    if data == {}:
        raise BadRequest("Reauset body must be full JSON")
    
    title = data["title"]
    
    if not isinstance(title, str):
        raise BadRequest("Title must be a string")
    
    if not title.strip():
        raise UnprocessableEntity("Title cannot be empty")

    todo = {
        "id": uuid.uuid4(),
        "title": title.strip(),
        "done": False
    }        
    
    todos.append(todo)
    return jsonify({
        "success": True,
        "data": todo
    })
    
if __name__ == "__main__":
    app.run(debug=True)