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

hitterDataReader = csv.DictReader(open(hitters_values_file), delimiter=',', quotechar='"')
# next(hitterDataReader, None)
for row in hitterDataReader:
    fangraphsid = row['PlayerId'].strip()
    # print(fangraphsid)
    existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
    if existing_player:
        existing_player.value = row['Dollars'].strip()
        if 'Adjusted' in row:
            if row['Adjusted'].strip() != '':
                existing_player.inflatedvalue = row['Adjusted'].strip()
            else:
                existing_player.inflatedvalue = 0
        else:
            existing_player.inflatedvalue = row['Dollars'].strip()
        existing_player.adp = row['ADP'].strip()
        # if fangraphsid == 'sa3022882':
        #     print(existing_player.value)
        #     print(existing_player.adp)
        existing_player.save()

pitcherDataReader = csv.DictReader(open(pitchers_values_file, encoding='utf-8'), delimiter=',', quotechar='"')
# next(pitcherDataReader, None)
for row in pitcherDataReader:
    fangraphsid = row['PlayerId'].strip()
    existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
    if existing_player:
        existing_player.value = row['Dollars'].strip()
        if row['Adjusted'].strip() != '':
            existing_player.inflatedvalue = row['Adjusted'].strip()
        else:
            existing_player.inflatedvalue = row['Dollars'].strip()
        existing_player.adp = row['ADP'].strip()
        existing_player.save()

hitterStatsDataReader = csv.DictReader(open(hitters_stats_file), delimiter=',', quotechar='"')
#next(hitterStatsDataReader, None)
for row in hitterStatsDataReader:
    fangraphsid = row['PlayerId'].strip()
    existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
    if existing_player:
        existing_player.stat1 = row['HR'].strip() 
        existing_player.stat2 = row['SB'].strip()
        existing_player.stat3 = row['RBI'].strip()
        existing_player.stat4 = row['R'].strip()
        existing_player.stat5 = row['AB'].strip()
        existing_player.stat6 = row['H'].strip()
        existing_player.save()
    # else:
    #     print("fangraphsId: {fid}".format(fid = fangraphsid))
    #     # print("fangraphsId: {row}".format(row = row))
        
pitcherStatsDataReader = csv.DictReader(open(pitchers_stats_file, encoding='utf-8'), delimiter=',', quotechar='"')
#next(pitcherStatsDataReader, None)
for row in pitcherStatsDataReader:
    fangraphsid = row['PlayerId'].strip()
    existing_player = Player.objects.all().filter(fangraphs_id = fangraphsid).first()
    if existing_player:
        existing_player.stat1 = row['W'].strip() 
        existing_player.stat2 = row['SV'].strip()
        existing_player.stat3 = row['SO'].strip()
        existing_player.stat4 = row['HLD'].strip()
        if row['IP'].strip() == '':
            existing_player.stat5 = 0
        else:
            existing_player.stat5 = row['IP'].strip()
        existing_player.stat6 = row['ER'].strip()
        existing_player.save()
adpReader = csv.reader(open(adp_file), delimiter=',')
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
