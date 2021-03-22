#!/bin/python3.7

from flask import Flask, request, jsonify, render_template
from pathlib import Path
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "eskdskkfdskfoo88493490iokol"


def check_secret():
    if 'Authorization' not in request.headers or \
            request.headers['Authorization'] != app.config['SECRET_KEY']:
        return False
    return True


@app.route('/', methods=['GET', 'POST'])
def index():
    datas = {}
    _folder = Path('datas')
    _folder.mkdir(parents=True, exist_ok=True)
    _, _, filenames = next(os.walk(_folder))
    for filename in filenames:
        try:
            with open(_folder / filename, "r") as f:
                datas[filename] = float(f.read())
        except FileNotFoundError:
            pass

    return render_template('index.html', datas=datas)


@app.route('/<variable>/<inc>')
def patch(variable, inc):
    if not check_secret():
        return {"message": "Invalid token"}, 401
    count = 0
    _folder = Path('datas')
    _folder.mkdir(parents=True, exist_ok=True)
    _file = _folder / Path(variable)
    try:
        with open(_file, "r") as f:
            count = float(f.read())
    except FileNotFoundError:
        pass
    count += float(inc)
    with open(_file, "w") as f:
        f.write(str(count))

    return str(count)


@app.route('/<variable>')
def get(variable):
    count = 0
    _folder = Path('datas')
    _folder.mkdir(parents=True, exist_ok=True)
    _file = _folder / Path(variable)
    try:
        with open(_file, "r") as f:
            count = float(f.read())
    except FileNotFoundError:
        pass

    return str(count)


@app.route('/<variable>/del')
def delete(variable):
    if not check_secret():
        return {"message": "Invalid token"}, 401
    _folder = Path('datas')
    _folder.mkdir(parents=True, exist_ok=True)
    _file = _folder / Path(variable)
    if os.path.exists(_file):
        os.remove(_file)

    return "deleted"
