import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from CTF import login, register, terms_conditions, privacy_policy, challenges_list, new, new_file


def create_app(test_config=None):
    global db
    # create and configure the app
    ALLOWED_EXTENSIONS = set(['rar','7z','zip','tar','tar.gz'])

    app = Flask(__name__, instance_relative_config=True)

    app.config['UPLOAD_FOLDER'] = 'upload/'

    app.config['SECRET_KEY'] = 'ctfx'
    # 设置数据库连接url
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mark:stone@localhost:3306/ctf_database'
    # 设置这一项是每次请求结束后都会自动提交数据库中的变动
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db = SQLAlchemy(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that test Flask run
    @app.route('/hello')
    def hello():
        return 'Test Flask run'

    from CTF import models

    from . import auth
    app.register_blueprint(login.bp)

    from . import auth
    app.register_blueprint(register.bp)

    from . import auth
    app.register_blueprint(privacy_policy.bp)

    from . import auth
    app.register_blueprint(terms_conditions.bp)

    from . import admin
    app.register_blueprint(challenges_list.bp)

    from . import admin
    app.register_blueprint(new.bp)

    from . import admin
    app.register_blueprint(new_file.bp)

    from . import challenges
    app.register_blueprint(challenges.bp)

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    return app
