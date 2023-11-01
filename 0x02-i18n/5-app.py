#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name)

babel = Babel(app)

# Set up the Babel configuration
class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)

# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

# Define a get_user function
def get_user(user_id):
    return users.get(user_id)

# Define the before_request function
@app.before_request
def before_request():
    user_id = request.args.get("login_as")
    g.user = get_user(int(user_id)) if user_id else None

# Language selector using request.accept_languages
@babel.localeselector
def get_locale():
    # Check if the user is logged in and has a defined locale, otherwise, use the default behavior
    if g.user and g.user["locale"] in app.config['LANGUAGES']:
        return g.user["locale"]
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    # Parametrize the templates using _() or gettext()
    title = _('home_title')
    header = _('home_header')
    welcome_message = _('logged_in_as', username=g.user["name"]) if g.user else _('not_logged_in')
    return render_template('5-index.html', title=title, header=header, welcome_message=welcome_message)

if __name__ == '__main__':
    app.run()
