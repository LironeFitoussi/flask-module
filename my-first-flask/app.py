from flask import Flask

from errors import register_error_handlers
from routes import tasks_bp

app = Flask(__name__)

app.register_blueprint(tasks_bp)
register_error_handlers(app)

if __name__ == "__main__":
    app.run(debug=True)
