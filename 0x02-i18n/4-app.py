#!/usr/bin/env python3
"""A Basic Flask app with internationalization support.
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
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> Optional[str]:
    """
    Determines the best match for this app's supported
    languages
    """
    translation_lang = request.args.get('locale')
    if translation_lang in app.config["LANGUAGES"]:
        return translation_lang
    return request.accept_languages.best_match(app.config["LANGUAGES"])

@app.route('/')
@app.route("/<string:locale>")
def get_index() -> str:
    """The home/index page.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
