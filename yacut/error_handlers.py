from flask import jsonify, render_template, request
from werkzeug.exceptions import HTTPException
from . import app


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def page_not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'message': 'Указанный id не найден'}), 404
    return render_template('404.html'), 404


def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


def handle_exception(error):
    if isinstance(error, HTTPException):
        return error
    app.logger.error(f"Unhandled Exception: {str(error)}")
    if request.path.startswith('/api/'):
        return jsonify({
            'message': 'Internal Server Error',
            'error': str(error)
        }), 500

    return render_template('500.html'), 500


def register_error_handlers(app):
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(InvalidAPIUsage, invalid_api_usage)
    app.register_error_handler(Exception, handle_exception)
