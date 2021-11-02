from re import T
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from werkzeug.exceptions import abort

from CTF.models import que,user,team
from CTF import login,db

bp = Blueprint('challenges', __name__)


@bp.route('/challenges', methods=['GET', 'POST'])
def challenges():
    if not login.myself:
        return redirect('auth/login')

    from CTF.models import db
    myself = user.query.filter(user.user_id == login.myself.user_id).first()

    if request.method == 'POST':
        id = request.form['id']
        flag = request.form['flag']
        print("id==>",id)
        print("flag==>", flag)

        t=0
        qu=0
        log=0
        q = que.query.filter(que.que_id == id).first()

        if q in myself.user_ans:                                 #如果做出来过则不再加分
            log=1

        if flag == q.que_flag:                           #答案正确
            print("true")
            if log:
                return jsonify({'code':1})
            myself.user_ans.append(q)
            myself.user_score += q.que_nowscore
            if myself.user_teamid:                              #如果有队伍进行数据库信息改动
                t=1
                print("team")
                myself_team = team.query.filter(team.team_id == myself.user_teamid).first()
                myself_team_ans = team.query.filter(team.team_ans.any(que.que_id == q.que_id)).first()
                if not myself_team_ans:
                    myself_team.team_ans.append(q)
                    myself_team.team_score +=q.que_nowscore
                
            if q.que_nowscore * 0.9 >= q.que_score * 0.75:      #如果分数未达下限进行分数改变
                print("score")
                qu=1
                q.que_nowscore *=0.9
               
            if t:
                db.session.add(myself_team)
                print("*********1")
            if qu:
                db.session.add(q)
                print("*********2")

            db.session.add(myself)
            db.session.commit()
            print("*********3")
            return jsonify({'code':1})

        else:                                                           #答案错误
            print("wrong")
            return jsonify({'code':0})




    challenges = [{
        'id': 0,
        'name': "test_challenges",
        'cate': "Web",
        'value': 100,
        'message': "MARK&STONE",
        'file': 'upload/123.zip'
    }]

    i = 1 
    q = None
    while 1:
        q = que.query.filter(que.que_id == i).first()
        if not q:
            break
        if q.que_state == 0:
            i+=1
            continue

        challenges.append({
        'id': q.que_id,
        'name': q.que_name,
        'cate': q.que_cate,
        'value': q.que_nowscore,
        'message': q.que_intro,
        'file': q.que_address
        })
        i += 1

    return render_template('challenges/challenges.html', challenges=challenges)