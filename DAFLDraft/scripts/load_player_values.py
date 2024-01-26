############ All you need to modify is below ############
hitters_values_file="./datafiles/hitters_values.csv"
pitchers_values_file="./datafiles/pitchers_values.csv"
hitters_stats_file="./datafiles/hitter_stats.csv"
pitchers_stats_file="./datafiles/pitcher_stats.csv"
your_djangoproject_home="C:../../"
############ All you need to modify is above ############

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='web_project.settings'

import django
django.setup()
from DAFLDraft.models import Player

import csv
hitterDataReader = csv.reader(open(hitters_values_file), delimiter=',', quotechar='"')
next(hitterDataReader, None)
for row in hitterDataReader:
    fangraphsid = row[13].strip()
    existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
    if existing_player:
        existing_player.value = row[12].strip()
        existing_player.adp = row[3].strip()
        existing_player.save()

pitcherDataReader = csv.reader(open(pitchers_values_file), delimiter=',', quotechar='"')
next(pitcherDataReader, None)
for row in pitcherDataReader:
    fangraphsid = row[13].strip()
    existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
    if existing_player:
        existing_player.value = row[12].strip()
        existing_player.adp = row[3].strip()
        existing_player.save()

hitterStatsDataReader = csv.reader(open(hitters_stats_file), delimiter=',', quotechar='"')
next(hitterStatsDataReader, None)
for row in hitterStatsDataReader:
    # print(row)
    fangraphsid = row[46].strip()
    existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
    if existing_player:
        existing_player.stat1 = row[9].strip() 
        existing_player.stat2 = row[19].strip()
        existing_player.stat3 = row[11].strip()
        existing_player.stat4 = row[10].strip()
        existing_player.stat5 = row[4].strip()
        existing_player.stat6 = row[5].strip()
        existing_player.save()
pitcherStatsDataReader = csv.reader(open(pitchers_stats_file), delimiter=',', quotechar='"')
next(pitcherStatsDataReader, None)
for row in pitcherStatsDataReader:
    fangraphsid = row[40].strip()
    existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
    if existing_player:
        existing_player.stat1 = row[2].strip() 
        existing_player.stat2 = row[8].strip()
        existing_player.stat3 = row[19].strip()
        existing_player.stat4 = row[9].strip()
        existing_player.stat5 = row[10].strip()
        existing_player.stat6 = row[14].strip()
        existing_player.save()
