from flask import render_template, redirect, url_for, flash
from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id
from flask import current_app as app


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    
    custom_id = form.custom_id.data
    if custom_id:
        # Проверка существования custom_id
        if URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!', 'error')
            return render_template('index.html', form=form)
    else:
        custom_id = get_unique_short_id()
    
    url_map = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(url_map)
    db.session.commit()
    
    # Передача полного URL в шаблон
    short_url = url_for('redirect_view', short=custom_id, _external=True)
    return render_template('index.html', form=form, short_url=short_url)

@app.route('/<short>')
def redirect_view(short):
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)
