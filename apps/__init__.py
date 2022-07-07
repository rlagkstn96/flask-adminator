# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import socketio



status = None
db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def flask_upload(app):
    @app.route('/upload')
    def render_file():
       return render_template('test.html')

    @app.route('/fileUpload', methods=['GET', 'POST'])
    def upload_file():
       if request.method == 'POST':
          f = request.files['file']
          ppath = os.getcwd()
          dir = ppath.replace("\\","/") + '/fileUpload/'
          f.save(dir + secure_filename(f.filename))
          return render_template('home/test.html')

    @app.route('/multifileUpload', methods=['GET', 'POST'])
    def multi_upload_file():
        if request.method == 'POST':
            upload = request.files.getlist("file[]")
            ppath = os.getcwd()
            dir = ppath.replace("\\", "/") + '/fileUpload/'
            for f in upload:
                f.save(dir + secure_filename(f.filename))
                status = "File uploaded"

        return render_template('home/test.html')





def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    flask_upload(app)
    return app
