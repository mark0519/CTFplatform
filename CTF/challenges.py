from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from CTF.models import que

bp = Blueprint('challenges', __name__)


@bp.route('/challenges')
def challenges():
    challenges = [{
        'id': 1,
        'name': "test_challenges",
        'cate': "Web",
        'value': 100,
        'message': "MARK&STONE",
        'file': 'upload/123.zip'
    }]
    challenges.append({
        'id': 1,
        'name': "test_PWN",
        'cate': "Pwn",
        'value': 150,
        'message': "pwner~",
        'file': 'upload/12334.zip'
    })
    challenges.append({
        'id': 1,
        'name': "test_PWN_2",
        'cate': "Pwn",
        'value': 200,
        'message': "pwner~ again",
        'file': 'upload/12333334.zip'
    })

    return render_template('challenges/challenges.html', challenges=challenges)