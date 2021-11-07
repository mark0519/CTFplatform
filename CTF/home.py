from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from CTF import login     

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    if login.myself:
        is_admin = 0
        if login.myself.user_teamid == 1:            #1表示是管理员
            is_admin = 1
        name = login.myself.user_name                #用户名信息
        return render_template('home/home.html', name=name , is_admin=is_admin)

    return render_template('home/home.html')




