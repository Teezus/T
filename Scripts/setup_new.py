'''
scripts

Contains a series of scripts used to load up the database.

@author: ameske
'''
from bs4 import BeautifulSoup
import urllib2
import datetime
import re
from app import db
from app import models

week_types = {1: 'A', 2: 'A', 3:'A', 4:'B', 5:'C', 6:'B', 7:'B', 8:'C', 9:'C', 10:'C', 11:'B', 12:'C', 13:'A', 14:'A', 15:'A', 16:'A', 17:'A' }
schedule_url = 'http://www.nfl.com/schedules/2013/REG'

def is_away_team(css_class):
  return css_class == "team-name away lost" or css_class == "team-name away "

def is_home_team(css_class):
  return css_class == "team-name home lost" or css_class == "team-name home "

def load_schedule():
  page = open('week17.html')
  scheduleHTML = BeautifulSoup(page.read())
        
  #PARALLEL LISTS OF AWAY, HOME, TIME
  away_teams_lost  = [ str(tag.string) for tag in scheduleHTML.find_all(class_="team-name away lost") ]
  home_teams_win   = [ str(tag.string) for tag in scheduleHTML.find_all(class_="team-name home ") ]
  print str(len(away_teams_lost)) + " - " + str(len(home_teams_win))
  away_teams_win   = [ str(tag.string) for tag in scheduleHTML.find_all(class_="team-name away ") ]
  home_teams_lost  = [ str(tag.string) for tag in scheduleHTML.find_all(class_="team-name home lost") ]
  print str(len(away_teams_win)) + " - " + str(len(home_teams_lost))

  times       = [ str(tag.string) for tag in scheduleHTML.find_all(class_="time") ]
  dates       = [ str(tag.find_previous(class_="schedules-list-date").contents[1].strings.next()).replace(',', '') for tag in scheduleHTML.find_all(class_="list-matchup-row-team") ]
          
  # SINCE WE ARE LATE TO THE PARTY, THE TIMES ARE NO LONGER VALID
  dates_times = zip(dates, times)
  dates = [ dt[0] + " 2013 " + "1:00" + " PM EST" for dt in dates_times ]
  datetimes = [ datetime.datetime.strptime(date_string, '%A %B %d %Y %I:%M %p %Z') for date_string in dates]
  print len(datetimes)
        
  # CREATE MATCHUP TUPLES AND THEN SEND THEM TO THE LOADING FUNCTION
  matchups1 = zip(away_teams_lost, home_teams_win, datetimes)
  matchups2 = zip(away_teams_win, home_teams_lost, datetimes)

  matchups = matchups1 + matchups2

  week = models.Week.query.filter_by(week=17).first()
  print str(week.id) + " - " + str(week.week)

  for matchup in matchups:
    home_team = models.Team.query.filter_by(nickname=matchup[1]).first()
    print str(home_team.id) + " - " + home_team.nickname
    away_team = models.Team.query.filter_by(nickname=matchup[0]).first()
    print str(away_team.id) + " - " + away_team.nickname
    new_matchup = models.Schedule(week=week, date=matchup[2], home_team=home_team, away_team=away_team)
    db.session.add(new_matchup)

  db.session.commit()

def main():
    load_schedule()
    
if __name__=='__main__':
    main()
    
