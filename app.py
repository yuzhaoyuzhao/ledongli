from flask import Flask
from admin import *

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/list')
def list():
    return 'list'


@app.route('/new')
def new():
    return 'new'


@app.route('/edit')
def edit():
    return 'edit'


@app.route('/detail')
def detail():
    return 'detail'


@app.route('/new')
def new():
    return 'new'


@app.route('/edit')
def edit():
    return 'edit'