#!nfl_env/bin/python
from app import app, manager
from flask.ext.migrate import MigrateCommand

app.debug = True
manager.run()
