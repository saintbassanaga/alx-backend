#!/usr/bin/env python3
"""ALX SE Backend I18N."""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    """Render hello world in the browser."""
    return render_template("0-index.html")


if __name__ == '__main__':
    app.run()
