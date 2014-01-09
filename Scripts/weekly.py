'''
Created on Aug 24, 2013

@author: ameske
'''
from bs4 import BeautifulSoup
import urllib2
from NFL.models import GameSchedule, Team, Pick, Participant

week_types = {1: 'A', 2: 'A', 3:'A', 4:'B', 5:'C', 6:'B', 7:'B', 8:'C', 9:'C', 10:'C', 11:'B', 12:'C', 13:'A', 14:'A', 15:'A', 16:'A', 17:'A' }
schedule_url = 'http://www.nfl.com/schedules/2013/REG'


def get_results(week_no):
    page = urllib2.urlopen(schedule_url + str(week_no))
    resultsHTML = BeautifulSoup(page.read())
    
    #WE CAN UNIQUELY ID A GAME BASED ON THE HOME TEAM, GATHER THEM AND THE SCORES
    home_teams          = [ str(tag.string) for tag in resultsHTML.find_all(class_="team-name home ") ]
    home_team_scores    = [ str(tag.string) for tag in resultsHTML.find_all(class_="team-score home ") ]
    away_team_scores    = [ str(tag.string) for tag in resultsHTML.find_all(class_="team-score away ") ]
    
    results = zip(home_teams, home_team_scores, away_team_scores)
    
    #UPDATE THE GAME SCHEDULE WITH THE APPROPRIATE SCORES
    for result in results:
        home_id = Team.objects.get(nickname=result[0])
        game = GameSchedule.objects.get(weekNumber=week_no, homeTeam=home_id)
        game.homeTeamScore = result[1]
        game.awayTeamScore = result[2]
        game.save()
    
    #NOW, SCORE THE USER PICKS
    score_games(week_no)

def score_games(week_no):
    #GATHER ALL OF THE PICKS FOR THE CURRENT WEEK
    weekly_picks = Pick.objects.filter(gameID__week__weekNumber=week_no)
    
    #FOR EACH PICK, CHECK WHO THE WINNING TEAM IS AND SCORE IT
    for pick in weekly_picks:
        pick.awarded_points = pick.points if pick.selection == pick.game.winner() else 0
        pick.save()
        

def create_picks(week_no):
    games = GameSchedule.objects.filter(week__weekNumber=week_no)
    users = Participant.objects.all()
    
    for current_user in users:
        for current_game in games:
            new_pick = Pick(participant=current_user, game=current_game, selection=None, points=0, awardedPoints=0)
            new_pick.save()