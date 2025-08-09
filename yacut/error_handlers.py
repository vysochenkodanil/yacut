from flask import render_template, current_app

def page_not_found(error):
    return render_template('404.html'), 404

def register_error_handlers(app):
    app.errorhandler(404)(page_not_found)