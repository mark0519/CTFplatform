# -*- coding: utf-8 -*-=

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from CTF import db

class user(db.Model):
    __tablename__ = 'user_data'
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    user_mail = db.Column(db.String(30), unique=True, nullable=False)
    user_pwd = db.Column(db.String(255), unique=True, nullable=False)
    user_teamid = db.Column(db.Integer, default=0)
    is_captain = db.Column(db.Boolean, default=0)
    # user_ans = db.Column(db.json)

    def __init__(self, name, mail, pwd):
        self.user_name = name
        self.user_mail = mail
        self.user_pwd = pwd

    def __repr__(self):
        return '<User %d>' % self.user_id


class team(db.Model):
    __tablename__ = 'team_data'
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(20), unique=True)
    team_capid = db.Column(db.Integer, default=0)
    team_intro = db.Column(db.Text)
    # team_member = db.Column(db.json)
    team_score = db.Column(db.Integer, default=0)
    # team_answer = db.Column(db.json)

    def __repr__(self):
        return '<User %d>' % self.team_id


class que(db.Model):
    __tablename__ = 'que_data'
    que_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    que_name = db.Column(db.String(20), unique=True)
    que_cate = db.Column(db.String(10), unique=True)
    que_flag = db.Column(db.String(64), unique=True)
    que_intro = db.Column(db.Text)
    que_address = db.Column(db.Text)
    que_score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %d>' % self.team_id




