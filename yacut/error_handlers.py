from http import HTTPStatus

from flask import jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from . import app


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        error_data = dict(self.payload or ())
        error_data['message'] = self.message
        return error_data


def page_not_found(error):
    if request.path.startswith('/api/'):
        return jsonify(
            {'message': 'Указанный id не найден'}
        ), HTTPStatus.NOT_FOUND
    return render_template('404.html'), HTTPStatus.NOT_FOUND


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
        }), HTTPStatus.INTERNAL_SERVER_ERROR

    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR


def register_error_handlers(app):
    app.register_error_handler(HTTPStatus.NOT_FOUND, page_not_found)
    app.register_error_handler(InvalidAPIUsage, invalid_api_usage)
    app.register_error_handler(Exception, handle_exception)
