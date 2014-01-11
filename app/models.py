from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

# Role constants
ROLE_USER = 0
ROLE_ADMIN = 1

# Game selection constants
HOME_TEAM = 0
AWAY_TEAM = 1


class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key = True)
  first_name = db.Column(db.String(25), index = True, nullable = False)
  last_name = db.Column(db.String(25), index = True, nullable = False)
  email = db.Column(db.String(120), index = True, unique = True, nullable = False)
  role = db.Column(db.SmallInteger, default = ROLE_USER, nullable = False)
  last_login = db.Column(db.DateTime)
  pwdhash = db.Column(db.String(100))
  picks = db.relationship('Pick', backref = 'user', lazy = 'dynamic')
  statistics = db.relationship('Statistic', backref = 'user', lazy = 'dynamic')

  def set_password(self, password):
    self.pwdhash = genereate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

  @classmethod
  def all(cls):
    return User.query.all()

  def __repr__(self):
    return '<User: %r, %r>' % self.first_name % self.last_name

class Year(db.Model):
  __tablename__ = 'year'
  id = db.Column(db.Integer, primary_key = True)
  year = db.Column(db.Integer, nullable = False)
  weeks = db.relationship('Week', backref = 'year', lazy = 'dynamic')
  statistics = db.relationship('Statistic', backref = 'year', lazy = 'dynamic')

  def __repr__(self):
    return '<Year: %d>' % self.year

class Week(db.Model):
  __tablename__ = 'week'
  id = db.Column(db.Integer, primary_key = True)
  week = db.Column(db.Integer, nullable = False, unique = True)
  year_id = db.Column(db.Integer, db.ForeignKey('year.id'))
  pvs_id = db.Column(db.Integer, db.ForeignKey('pointvalueset.id'))
  games = db.relationship('Schedule', backref = 'week', lazy = 'dynamic')
  statistics = db.relationship('Statistic', backref = 'week', lazy = 'dynamic')

  def __repr__(self):
    return '<Week: %d, %d>' % self.week % self.year

class PointValueSet(db.Model):
  __tablename__ = 'pointvalueset'
  id = db.Column(db.Integer, primary_key = True)
  type = db.Column(db.String(1), unique = True, nullable = False)
  seven = db.Column(db.Integer, nullable = False)
  five = db.Column(db.Integer, nullable = False)
  three = db.Column(db.Integer, nullable = False)
  one = db.Column(db.Integer, nullable = False)
  weeks = db.relationship('Week', backref = 'type', lazy = 'dynamic')
  
  def __repr__(self):
    return '<Week Type: %r>' % self.type


class Team(db.Model):
  __tablename__ = 'team'
  id = db.Column(db.Integer, primary_key = True)
  city = db.Column(db.String(50), index = True, nullable = False)
  nickname = db.Column(db.String(50), index = True, nullable = False)
  stadium = db.Column(db.String(100), nullable = False)

  @classmethod
  def all(cls):
    return Team.query.all()

  def __repr__(self):
    return '<Team: %r %r>' % self.city % self.nickname


class Schedule(db.Model):
  __tablename__ = 'schedule'
  id = db.Column(db.Integer, primary_key = True)
  week_id = db.Column(db.Integer, db.ForeignKey('week.id'), nullable = False)
  date = db.Column(db.DateTime, nullable = False)
  home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = False)
  home_team_score = db.Column(db.Integer, default=-1)
  away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = False)
  away_team_score = db.Column(db.Integer, default=-1)
  picks = db.relationship('Pick', backref = 'game', lazy = 'dynamic')
  home_team = db.relationship(Team, foreign_keys=home_team_id)
  away_team = db.relationship(Team, foreign_keys=away_team_id)

  @property
  def winner(self):
    return HOME_TEAM if self.home_team_score > self.away_team_score else AWAY_TEAM
  
  def __repr__(self):
    return '<Game: %r at %r on %r>' % self.away_team % self.home_team % self.date


class Pick(db.Model):
  __tablename__ = 'pick'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
  game_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable = False)
  selection = db.Column(db.SmallInteger)
  points = db.Column(db.Integer)
  awardedPoints = db.Column(db.Integer, default = 0)

  @classmethod
  def user_picks_by_week(cls, user, week):
    return Pick.query.join(Schedule).filter(Schedule.week == week, Pick.user == user).all()

  def __repr__(self):
    return '<Pick: %r - %d - %d>' % self.user % self.game % self.selection
  
# A note about this table. This techincally can be calculated from the database.
# However, this information will be accessed frequently on the statistics page
# of the pool and of a user, so explicity creating it here in a table will
# save the overhead of having to join every time someone wants to look at their
# statistics.
class Statistic(db.Model):
  __tablename__ = 'statistics'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
  year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable = False)
  week_id = db.Column(db.Integer, db.ForeignKey('week.id'), nullable = False)
  seven = db.Column(db.Integer, default = 0)
  five = db.Column(db.Integer, default = 0)
  three = db.Column(db.Integer, default = 0)
  one = db.Column(db.Integer, default = 0)

  def __repr__(self):
    return '<Statistic: %r>' % self.user
