# -*- coding: utf-8 -*-=
from CTF import db
from CTF.models import user

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

bp = Blueprint('/admin/challenges_list', __name__)


@bp.route('/admin/challenges_list', methods=['GET'])
def challenges_list():
    return render_template('admin/challenges_list.html')
