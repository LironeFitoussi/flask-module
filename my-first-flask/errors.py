from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound, BadRequest, UnprocessableEntity

errors_bp = Blueprint("errors", __name__)
@errors_bp.app_errorhandler(NotFound)
def handle_type_error(e):
    return jsonify({
        "error": str(e)
    }), 404

@errors_bp.app_errorhandler(BadRequest)
def handle_type_error(e):
    return jsonify({
        "error": str(e)
    }), 400
    
@errors_bp.app_errorhandler(UnprocessableEntity)
def handle_type_error(e):
    return jsonify({
        "error": str(e)
    }), 422