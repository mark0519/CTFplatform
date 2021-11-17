# -*- coding: utf-8 -*-=
from CTF import db
from CTF.models import user

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

bp = Blueprint('/auth/privacy_policy', __name__)


@bp.route('/auth/privacy_policy', methods=['GET'])
def pp():
    return render_template('auth/privacy_policy.html')
