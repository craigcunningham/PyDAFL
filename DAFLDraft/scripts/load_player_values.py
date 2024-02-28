#Consider converting all the CSV files to dictionaries. It would make it much more readable and robust against file changes

############ All you need to modify is below ############
hitters_values_file="./datafiles/hitters_values.csv"
pitchers_values_file="./datafiles/pitchers_values.csv"
hitters_stats_file="./datafiles/hitter_stats.csv"
pitchers_stats_file="./datafiles/pitcher_stats.csv"
adp_file="./datafiles/nfbc-adp.csv"
player_id_map_file="./datafiles/player_id_map.csv"
your_djangoproject_home="C:../../"
############ All you need to modify is above ############

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='web_project.settings'

import django
django.setup()
from DAFLDraft.models import Player

import csv
with open(player_id_map_file, 'r', encoding='utf-8') as f:
    dict_reader = csv.DictReader(f)
    player_id_map = list(dict_reader)

hitterDataReader = csv.reader(open(hitters_values_file), delimiter=',', quotechar='"')
next(hitterDataReader, None)
for row in hitterDataReader:
    fangraphsid = row[13].strip()
    # print(fangraphsid)
    existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
    if existing_player:
        existing_player.value = row[12].strip()
        existing_player.adp = row[3].strip()
        # if fangraphsid == 'sa3022882':
        #     print(existing_player.value)
        #     print(existing_player.adp)
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
adpReader = csv.reader(open(adp_file), delimiter='\t')
next(adpReader, None)
for row in adpReader:
    nfbcid = row[1].strip()
    player = next((item for item in player_id_map if item["NFBCID"] == nfbcid), False)
    if player != False:
        fangraphsid = player["IDFANGRAPHS"]
        existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
        if existing_player:
            existing_player.adp = row[0]
            existing_player.save()
