# -*- coding: utf-8 -*-=
from CTF import db
from CTF.models import user

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

bp = Blueprint('/auth/terms_conditions', __name__)


@bp.route('/auth/terms_conditions', methods=['GET'])
def tc():
    return render_template('auth/terms_conditions.html')
