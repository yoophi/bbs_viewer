from flask import render_template

from bbs_viewer.core import main


@main.route('/')
def index():
    return render_template('index.html')
