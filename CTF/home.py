from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from CTF import login     

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    if login.myself:
        name = login.myself.user_name         #用户名信息
        # return render_template('home/home.html', name)

    return render_template('home/home.html')