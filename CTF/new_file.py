# -*- coding: utf-8 -*-=
import os

from werkzeug.utils import secure_filename

from CTF import db
from CTF.models import user

import hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify,
)
from werkzeug.exceptions import abort

bp = Blueprint('/admin/new_file', __name__)


@bp.route('/admin/new_file', methods=['POST'])
def challenges_list():
    if request.method == 'POST':
        file = request.form.get('file')
        print(request.files)
        file.save(os.path.join('upload/', secure_filename(file.filename)))

