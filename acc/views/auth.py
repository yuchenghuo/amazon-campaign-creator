import flask
import requests

import acc


@acc.app.route('/login/')
def login():
    """Display / route."""
    if is_logged_in() and valid_secrets():
        return flask.redirect(flask.url_for('index'))
    return flask.render_template("login.html")


@acc.app.route('/accounts/', methods=['POST'])
def edit_account():
    """Display / route."""
    operation = flask.request.values.get('operation')
    if operation == 'login':
        client_id = flask.request.values.get('client_id')
        client_secret = flask.request.values.get('client_secret')
        refresh_token = flask.request.values.get('refresh_token')
        flask.session['client_id'] = client_id
        flask.session['client_secret'] = client_secret
        flask.session['refresh_token'] = refresh_token
        if valid_secrets():
            return flask.render_template("index.html")
        flask.session.clear()
        return flask.redirect(flask.url_for('login'))


@acc.app.route('/logout/', methods=['POST'])
def logout():
    """Display / route."""
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))


@acc.app.route('/secrets/', methods=['GET'])
def get_secrets():
    """Display / route."""
    if not is_logged_in():
        return {'error': 'Not logged in'}
    get_access_token()
    return flask.jsonify(flask.session)


@acc.app.route('/profiles/', methods=['GET'])
def get_profiles():
    """Display / route."""
    if not is_logged_in():
        return {'error': 'Not logged in', 'profiles': []}
    get_access_token()
    r = requests.get(
        'https://advertising-api.amazon.com/v2/profiles',
        headers={
            'Amazon-Advertising-API-ClientId': flask.session['client_id'],
            'Authorization': 'Bearer ' + flask.session['access_token']
        },
    )
    response = {
        'profiles': r.json(),
    }
    return flask.jsonify(response)


@acc.app.route('/login_status/', methods=['GET'])
def get_login_status():
    """Display / route."""
    return flask.jsonify({
        'logged_in': 'true' if is_logged_in() and valid_secrets() else 'false'})


def get_access_token():
    """Get access token from Amazon API."""
    r = requests.post(
        'https://api.amazon.com/auth/o2/token',
        data={
            'grant_type': 'refresh_token',
            'client_id': flask.session['client_id'],
            'refresh_token': flask.session['refresh_token'],
            'client_secret': flask.session['client_secret'],
        },
    )
    if r.status_code == 200:
        flask.session['access_token'] = r.json()['access_token']
    else:
        flask.session.clear()
        raise Exception


def is_logged_in():
    if not all(x in flask.session for x in
               ['client_id', 'client_secret', 'refresh_token']):
        return False
    return True


def valid_secrets():
    try:
        get_access_token()
    except Exception:
        flask.session.clear()
        return False
    return True
