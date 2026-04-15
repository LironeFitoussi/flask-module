from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "API is running"
    })

@app.route("/status")
def status():
    return jsonify({
        "status": "Ok",
        "version": "1.0.0"
    })

@app.route("/time")
def current_time():
    now = datetime.now(timezone.utc).isoformat()
    return jsonify({
        "time": now
    })


@app.route("/info")
def info():
    return jsonify({
        "app": "Flask Practice",
        "author": "Student",
        "day": 2
    })

@app.route("/echo", methods=["POST"])
def echo():
    body = request.json
    
    if not bool(body) :
        return jsonify({
            "success": False,
            "error": "JSON body required"
        }), 400
    
    return jsonify({
        "success": True,
        "echo": body
    })
    
USERS = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30, "role": "admin"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25, "role": "user"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "age": 35, "role": "user"},
    {"id": 4, "name": "Alice Smith", "email": "alice.smith@example.com", "age": 28, "role": "moderator"},
]


@app.route("/search")
def search():
    name = request.args.get("name")
    
    if not name:
        return jsonify({
            "success": False,
            "error": "name is required"
        }), 400
    
    results = []
    for u in USERS:
        if name in u["name"]:
            results.append(u)
    
    
    return jsonify({
        "success": True,
        "results": results
    })
    

if __name__ == "__main__":
    app.run(debug=True)