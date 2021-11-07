from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from CTF import login

bp = Blueprint('/admin/edit_teams', __name__)


@bp.route('/admin/edit_teams', methods=['GET','POST'])
def feteams():
    if not login.myself or login.myself.user_teamid !=1:
        return redirect('../auth/login')

    return render_template('admin/edit_teams.html')