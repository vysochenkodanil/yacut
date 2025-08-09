import re
from flask import Blueprint, jsonify, request
from . import db
from .models import URLMap
from .utils import get_unique_short_id
from .error_handlers import InvalidAPIUsage

bp_api = Blueprint('api', __name__)


@bp_api.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if custom_id:
        if len(custom_id) > 16:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if not re.fullmatch(r'[A-Za-z0-9]+', custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if URLMap.query.filter_by(short=custom_id).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
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
    }), 201


@bp_api.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
