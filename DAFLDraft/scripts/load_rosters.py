############ All you need to modify is below ############
# non rostered players
# hitters_file="./datafiles/freeagenthitters.csv"
# pitchers_file="./datafiles/freeagentpitchers.csv"
all_players_file="./datafiles/rosters.csv"
# rostered players
rostered_file="./datafiles/rosteredplayers.csv"
# files = [hitters_file, pitchers_file, rostered_file]
files = [all_players_file]
# Full path to the directory immediately above your django project directory
your_djangoproject_home="C:../../"
############ All you need to modify is above ############

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='web_project.settings'

import django
django.setup()
from DAFLDraft.models import Player, Roster, Team

import csv
for file in files:
    dataReader = csv.reader(open(file, encoding='utf-8'), delimiter=',', quotechar='"')

    for row in dataReader:
        roster = Roster()
        roster.team_id = row[0].strip()
        roster.player_id = row[1].strip()
        # roster.team = Team.objects.all().filter(id = row[0].strip()).first()
        # roster.player = Player.objects.all().filter(id = row[1].strip()).first()
        roster.position = row[2].strip()
        roster.salary = row[3].strip()
        roster.contract_year = row[4].strip()
        roster.save()
        