from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

# Create the flask application
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy()
db.app = app
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

from app import views
from app import models
