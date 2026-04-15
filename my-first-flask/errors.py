from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({
            "error": error.name,
            "message": error.description,
            "status": error.code,
        }), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unhandled exception: %s", error)
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred.",
            "status": 500,
        }), 500
