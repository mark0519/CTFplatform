from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify,session
)
from werkzeug.exceptions import abort
from CTF.models import user,team
from CTF import login,db

bp = Blueprint('/join_teams', __name__)


@bp.route('/join_teams', methods=['GET','POST'])
def join_teams():
    # 'tid=' + tid
    if user.query.filter(user.user_id == session.get('id')).first().user_teamid !=None:               #已经有队伍
        return jsonify({'code': 0}),200

    if request.method == 'POST':
        tid = request.form['tid']
        print(tid)
        myself = user.query.filter(user.user_id ==session.get('id')).first()
        myself.user_teamid = tid
        myself.is_captain = -1
        db.session.add(myself)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    return redirect('teams')