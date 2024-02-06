#!/usr/bin/env python3
"""
0. Basic Flask app
"""
from flask_babel import Babel
from flask import Flask, render_template, request


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Retrieves the locale for a web page.
    """
    for parameter in request.query_string.decode('utf-8').split('&'):
        key, value = parameter.split('=')
        if key == 'locale' and value in app.config["LANGUAGES"]:
            return value
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/", strict_slashes=False)
def home_page():
    """Displays the index page"""
    try:
        return render_template("4-index.html")
    except ValueError:
        pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
