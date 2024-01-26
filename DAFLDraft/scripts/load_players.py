############ All you need to modify is below ############
# non rostered players
# hitters_file="./datafiles/freeagenthitters.csv"
# pitchers_file="./datafiles/freeagentpitchers.csv"
all_players_file="./datafiles/all_players.csv"
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
from DAFLDraft.models import Player

import csv
for file in files:
    dataReader = csv.reader(open(file), delimiter=',', quotechar='"')

    for row in dataReader:
        cbsid = row[1].strip()
        existing_player = Player.objects.all().filter(cbs_id = cbsid).first()
        if existing_player:
            existing_player.name = row[0].strip()
            existing_player.cbs_id = row[1].strip()
            existing_player.fangraphs_id = row[2].strip()
            existing_player.mlb_id = row[3].strip()
            existing_player.eligible_positions = row[4].strip()
            existing_player.save()
        else:
            player = Player()
            player.name = row[0].strip()
            player.cbs_id = row[1].strip()
            player.fangraphs_id = row[2].strip()
            player.mlb_id = row[3].strip()
            player.eligible_positions = row[4].strip()
            player.save()
