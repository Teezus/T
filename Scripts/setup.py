'''
scripts

Contains a series of scripts used to load up the database.

@author: ameske
'''
from bs4 import BeautifulSoup
import urllib2
import datetime
from NFL.models import GameSchedule, Team, PointValueSet, Pick, Week

week_types = {1: 'A', 2: 'A', 3:'A', 4:'B', 5:'C', 6:'B', 7:'B', 8:'C', 9:'C', 10:'C', 11:'B', 12:'C', 13:'A', 14:'A', 15:'A', 16:'A', 17:'A' }
schedule_url = 'http://www.nfl.com/schedules/2013/REG'


def load_schedule():
    for week_no in range(1, 18):
        
        #OPEN UP THE HTML FOR EACH WEEK
        print 'Current Week: ' + str(week_no) 
        page = urllib2.urlopen(schedule_url + str(week_no))
        scheduleHTML = BeautifulSoup(page.read())
                        
        #PARALLEL LISTS OF AWAY, HOME, TIME
        away_teams  = [ str(tag.string) for tag in scheduleHTML.find_all(class_="team-name away ") ]
        home_teams  = [ str(tag.string) for tag in scheduleHTML.find_all(class_="team-name home ") ]
        times       = [ str(tag.string) for tag in scheduleHTML.find_all(class_="time") ]
        dates       = [ str(tag.find_previous(class_="schedules-list-date").contents[1].strings.next()).replace(',', '') for tag in scheduleHTML.find_all(class_="list-matchup-row-team") ]
                        
        #MERGE times and dates AND THEN BRING BACK INTO A DATETIME LIST
        dates_times = zip(dates, times)
        dates       = [ dt[0] + " 2013 " + dt[1] + " PM EST" for dt in dates_times]
        datetimes = [ datetime.datetime.strptime(date_string, '%A %B %d %Y %I:%M %p %Z') for date_string in dates ]
        
        #CREATE MATCHUP TUPLES AND THEN SEND THEM TO THE LOADING FUNCTION
        matchups = zip(away_teams, home_teams, datetimes)      
        for matchup in matchups:
            add_matchup(matchup, week_no)
            

def add_matchup(matchup_tuple, week_no):
    
    week = Week.objects.get(weekNumber=week_no)
    away = Team.objects.get(nickname=matchup_tuple[0])
    home = Team.objects.get(nickname=matchup_tuple[1])
    
    new_matchup = GameSchedule(week=week, date=matchup_tuple[2], awayTeam=away, homeTeam=home, awayTeamScore=-1, homeTeamScore=-1)
    new_matchup.save()

   
def main():
    load_schedule()
    
if __name__=='__main__':
    main()
    