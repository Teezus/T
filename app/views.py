from flask import render_template, request, session, url_for, redirect
from app import app, db
from models import Team, User, Week, Schedule, Year, Pick, TBP
from forms import SigninForm
import datetime


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/teams')
def teams():
  teams = Team.all()
  return render_template('teams.html', teams=teams)


@app.route('/profile')
def profile():
  # Redirect the user to login if they currently aren't.
  if 'email' not in session:
    return redirect(url_for('signin'))
  
  user = User.query.filter_by(email=session['email']).first()
  if user:
    return render_template('profile.html', user=user)
  else:
    return render_template('error.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  
  #POST means that they are signing in 
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      user = User.query.filter_by(email=form.email.data).first()
      user.last_seen = datetime.datetime.now()
      db.session.commit()
      return redirect(url_for('profile'))
  #GET means that they want to login
  elif request.method == 'GET':
    return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
  if 'email' not in session:
    return redirect(url_for('signin'))
  session.pop('email', None)
  return redirect(url_for('index'))


@app.route('/schedule')
def schedule():
  years = Year.all()
  return render_template('schedule.html', years=years)


@app.route('/schedule/<int:year>')
def year_schedule(year):
  weeks = Week.query.join(Year).filter(Year.year == year).all()
  return render_template('year_schedule.html', weeks=weeks, year=year)


@app.route('/schedule/<int:year>/<int:week>')
def week_schedule(year, week):
  week = Week.query.join(Year).filter(Year.year==year, Week.week==week).first()
  week_games = week.games
  return render_template('week_schedule.html', games=week_games)


@app.route('/picks')
def make_picks():
  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email=session['email']).first()
  if user:
    picks = Pick.query.filter_by(user=user, selection=TBP)
    return render_template('picks.html', picks=picks)
  else:
    return render_template('error.html')

@app.route('/dynamic_picks')
def make_picks_dynamic():
  print "STUB"

@app.route('/standings')
def standings():
  return render_template('standings.html')
