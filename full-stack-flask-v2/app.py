from flask import Flask, render_template

from config.db import init_db
from config.errors import errors_bp
from routes.lists import lists_bp
from routes.tasks import tasks_bp

app = Flask(__name__)

init_db(app)

app.register_blueprint(lists_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(errors_bp)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
