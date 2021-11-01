# -*- coding: utf-8 -*-=

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from CTF import db

teams_ans=db.Table('teams_ans',
    db.Column('team_id',db.Integer,db.ForeignKey('team_data.team_id')),
    db.Column('que_id',db.Integer,db.ForeignKey('que_data.que_id'))
)

users_ans = db.Table('users_ans',
    db.Column('user_id',db.Integer,db.ForeignKey('user_data.user_id')),
    db.Column('que_id',db.Integer,db.ForeignKey('que_data.que_id'))
)

class user(db.Model):
    __tablename__ = 'user_data'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    user_mail = db.Column(db.String(30), unique=True, nullable=False)
    user_pwd = db.Column(db.String(255), nullable=False)
    user_teamid = db.Column(db.Integer, db.ForeignKey('team_data.team_id'))
    is_captain = db.Column(db.Boolean, default=0)
    user_state = db.Column(db.Boolean, default=1)
    user_ans=db.relationship('que',
                            secondary=users_ans,
                            backref=db.backref('user',lazy='dynamic'),
                            lazy='dynamic')

    def __init__(self, name, mail,pwd):
        self.user_name = name
        self.user_mail = mail
        self.user_pwd = pwd

    def __repr__(self):
        return '<User %d>' % self.user_id


class team(db.Model):
    __tablename__ = 'team_data'
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(20), unique=True,nullable=False)
    team_capid = db.Column(db.Integer, default=0)
    team_intro = db.Column(db.Text)
    team_score = db.Column(db.Integer, default=0)
    team_state = db.Column(db.Boolean, default=1)
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
    que_name = db.Column(db.String(20))
    que_cate = db.Column(db.String(10))
    que_flag = db.Column(db.String(64))
    que_intro = db.Column(db.Text)
    que_state = db.Column(db.Boolean, default=1)
    que_address = db.Column(db.Text)
    que_score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Question %d>' % self.que_id
    def __init__(self,name,cate,flag,intro,hidden,score):
        self.que_name=name
        self.que_cate=cate
        self.que_flag=flag
        self.que_intro=intro
        self.que_hidden=hidden
        self.que_score=score