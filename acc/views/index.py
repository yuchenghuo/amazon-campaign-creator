"""
Amazon campaign creator index (main) view.

URLs include:
/
"""
import flask

import acc
from acc.views.auth import valid_secrets


@acc.app.route('/')
def index():
    if not valid_secrets():
        return flask.redirect(flask.url_for('login'))
    return flask.render_template("index.html")
