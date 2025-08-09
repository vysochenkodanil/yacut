from flask import render_template

def page_not_found(error):
    return render_template('404.html'), 404

def register_error_handlers(app):
    app.register_error_handler(404, page_not_found)