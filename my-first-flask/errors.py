from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnprocessableEntity
from flask import jsonify, Blueprint

errors_bp = Blueprint("errrors",__name__)
# create errorhundle for not found errors
@errors_bp.errorhandler(NotFound)
def not_found(e):
    return jsonify({
        "ERROR": str(e)
    }), 404

# create errorhundle forBadrequest errors  
@errors_bp.errorhandler(BadRequest)
def bad_request(e):
    return jsonify({
        "ERROR": str(e)
    }), 400

# create errorhundle forunprocessable entries errors
@errors_bp.errorhandler(UnprocessableEntity)
def empty_strings(e):
    return jsonify({
        "ERROR": str(e)
    }), 422