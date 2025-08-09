from flask import Blueprint, render_template, redirect, url_for
from yacut import db
from .models import URLMap
from .forms import URLForm
from .utils import get_unique_short_id

bp = Blueprint('views', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data or get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(url_map)
        db.session.commit()
        short_url = url_for(
            'views.redirect_view', short=custom_id, _external=True
        )
        return render_template('index.html', form=form, short_url=short_url)

    return render_template('index.html', form=form)


@bp.route('/<short>')
def redirect_view(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
