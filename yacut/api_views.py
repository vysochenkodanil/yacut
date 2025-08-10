from http import HTTPStatus

from flask import Blueprint, jsonify, request

from . import db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id, validate_short_id

bp_api = Blueprint('api', __name__)


@bp_api.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        try:
            validate_short_id(custom_id)
        except ValueError as e:
            raise InvalidAPIUsage(str(e))
    else:
        custom_id = get_unique_short_id()

    url_map = URLMap(
        original=data['url'],
        short=custom_id
    )
    db.session.add(url_map)
    db.session.commit()

    return jsonify({
        'url': url_map.original,
        'short_link': request.host_url + custom_id
    }), HTTPStatus.CREATED


@bp_api.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
