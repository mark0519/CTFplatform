from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from werkzeug.exceptions import abort
from CTF.models import user,team
from CTF import login,db

bp = Blueprint('/join_teams', __name__)


@bp.route('/join_teams', methods=['GET','POST'])
def join_teams():
    # 'tid=' + tid
    if login.myself.user_teamid!=None:                  #已经有队伍
        return jsonify({'code': 0}),200

    if request.method == 'POST':
        tid = request.form['tid']
        print(tid)
        myself = user.query.filter(user.user_id ==login.myself.user_id).first()
        myself.user_teamid = tid
        db.session.add(myself)
        db.session.commit()

    return redirect('teams')