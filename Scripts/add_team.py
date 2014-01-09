from app import db, models

team_data = open('Scripts/teams.txt', 'r')

for line in team_data:
  line = line.strip()
  split_line = line.split(',')
  new_team = models.Team(city=split_line[0], nickname=split_line[1], stadium=split_line[2])
  db.session.add(new_team)

db.session.commit()
team_data.close()
