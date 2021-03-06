import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_relative_config=True)

app.config['UPLOAD_FOLDER'] = 'upload/'

app.config['SECRET_KEY'] = 'ctfx'
    # 设置数据库连接url
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://adm1n:mark&stone@localhost:3306/ctf_database?autocommit=true'
    # 设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

teams_ans=db.Table('teams_ans',
    db.Column('team_id',db.Integer,db.ForeignKey('team_data.team_id')),
    db.Column('que_id',db.Integer,db.ForeignKey('que_data.que_id'))
)

users_ans = db.Table('users_ans',
    db.Column('user_id',db.Integer,db.ForeignKey('user_data.user_id')),
    db.Column('que_id',db.Integer,db.ForeignKey('que_data.que_id')),
)

class user(db.Model):
    __tablename__ = 'user_data'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    user_mail = db.Column(db.String(30), unique=True, nullable=False)
    user_pwd = db.Column(db.String(255), nullable=False)
    user_teamid = db.Column(db.Integer, db.ForeignKey('team_data.team_id'))
    is_captain = db.Column(db.Integer, default=0)
    user_state = db.Column(db.Integer, default=1)
    user_score = db.Column(db.Integer, default=0)
    user_ans=db.relationship('que',
                            secondary=users_ans,
                            backref=db.backref('user',lazy='dynamic'),
                            lazy='dynamic')


    def __init__(self, name, mail,pwd,team_id,is_captain,user_state,user_score):
        self.user_name = name
        self.user_mail = mail
        self.user_pwd = pwd
        self.user_teamid = team_id
        self.is_captain = is_captain
        self.user_state=user_state
        self.user_score = user_score

    def __repr__(self):
        return '<User %d>' % self.user_id


class team(db.Model):
    __tablename__ = 'team_data'
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(20), unique=True,nullable=False)
    team_capid = db.Column(db.Integer, default=0)
    team_intro = db.Column(db.Text)
    team_score = db.Column(db.Integer, default=0)
    team_state = db.Column(db.Integer, default=1)
    team_sum = db.Column(db.Integer,default = 1)
    team_ans=db.relationship('que',
                            secondary=teams_ans,
                            backref=db.backref('team',lazy='dynamic'),
                            lazy='dynamic')
    team_member = db.relationship('user',backref='member')

    def __repr__(self):
        return '<Team %d>' % self.team_id


class que(db.Model):
    __tablename__ = 'que_data'
    que_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    que_name = db.Column(db.String(20) , unique=True)
    que_cate = db.Column(db.String(10))
    que_flag = db.Column(db.String(64))
    que_intro = db.Column(db.Text)
    que_state = db.Column(db.Integer, default=1)
    que_address = db.Column(db.Text)
    que_score = db.Column(db.Integer, default=0)
    # que_nowscore = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Question %d>' % self.que_id
    def __init__(self,name,cate,flag,intro,hidden,score):
        self.que_name=name
        self.que_cate=cate
        self.que_flag=flag
        self.que_intro=intro
        self.que_hidden=hidden
        self.que_score=score


db.drop_all()
db.create_all()
print("******1")
new_team = team(team_name = 'adm1ns',team_capid = 1,team_intro = '',team_score = 0,team_state = 0,team_sum=1)
new_user = user('adm1n','adm1n@adm1n.com','d9a27a55077cb6a913c385757dfd6504',1,1,0,0)
print("******2")
db.session.add(new_team)
print("******3")
try:
    db.session.commit()
except:
    db.session.rollback()
    raise
finally:
    db.session.close()
print("******4")
db.session.add(new_user)
print("******5")
try:
    db.session.commit()
except:
    db.session.rollback()
    raise
finally:
    db.session.close()
print("******6")
print("初始化成功")
