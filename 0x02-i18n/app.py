#!/usr/bin/env python3
"""ALX SE Backend I18N."""
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
from typing import Union, Mapping
import pytz
from datetime import datetime


class Config(object):
    """Configuration for babel."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Return the best match of locale to use."""
    locale = request.args.get('locale')
    if locale:
        return locale
    if g.user:
        locale = g.user.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> Union[str, None]:
    """Return the user timezone."""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            tzone = pytz.timezone(timezone)
            return tzone.zone
        except pytz.exceptions.UnknownTimeZoneError:
            return None
    if g.user:
        timezone = g.user.get('timezone')
        try:
            tzone = pytz.timezone(timezone)
            return tzone.zone
        except pytz.exceptions.UnknownTimeZoneError:
            return None


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Return a dict of user info or None."""
    param = request.args.get('login_as')
    if not param:
        return None
    user_id = int(param)
    user = users.get(user_id)
    return user


@app.before_request
def before_request():
    """Set user."""
    user = get_user()
    g.user = user


@app.route('/')
def index():
    g.time = format_datetime(datetime.now())
    """Render hello world in the browser."""
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
