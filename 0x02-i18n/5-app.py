#!/usr/bin/env python3
"""
0. Basic Flask app
"""
from flask_babel import Babel
from flask import Flask, render_template, request, g

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


def get_user():
    """Retrieves a user from the user 'database' based on a user id.
    """
    try:
        user_id = request.args.get('login_as', None)
        return users.get(int(user_id), None) if user_id is not None else None
    except Exception:
        return None


@app.before_request
def before_request() -> None:
    """Try to resolve the user making this request based on the request
    parameters 'login_as'.
    """
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Retrieves the locale for a web page.
    """
    for parameter in request.query_string.decode('utf-8').split('&'):
        try:
            key, value = parameter.split('=')
            if key == 'locale' and value in app.config["LANGUAGES"]:
                return value
        except ValueError:
            continue
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/", strict_slashes=False)
def home_page():
    """Displays the index page"""
    try:
        return render_template("5-index.html")
    except ValueError as exception:
        print(exception.__str__())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
