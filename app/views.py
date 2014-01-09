from flask import render_template
from app import app
from models import Team

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/teams')
def teams():
  teams = Team.all()
  return render_template('teams.html', teams=teams)
