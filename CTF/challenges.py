from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('challenges', __name__)


@bp.route('/challenges')
def challenges():
    return render_template('challenges/challenges.html')