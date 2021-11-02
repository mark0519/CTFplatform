from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from CTF.login import myself        #存储用户信息

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    name = myself.user_name         #用户名信息
    return render_template('home/home.html')