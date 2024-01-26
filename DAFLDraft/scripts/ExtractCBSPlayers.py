# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 17:46:03 2021

@author: ccunningham
"""


from csv import DictReader
# open file in read mode
with open("./datafiles/player_id_map.csv", 'r') as f:
    dict_reader = DictReader(f)
    player_id_map = list(dict_reader)
# import urllib.request
# page = urllib.request.urlopen('https://dafl.baseball.cbssports.com/stats/stats-main/all:C:1B:2B:3B:SS:OF:U:P/period-1:p/All+Batters+with+Eligibility')
# print(page.read())

fileName = "./datafiles/AllPlayersEligibility.html"
output = open("./datafiles/all_players.csv", "w")
output2 = open("./datafiles/nocbsid.csv", "w")

with open(fileName, "rt") as file:
    Lines = file.readlines()
 
count = 0
# Strips the newline character
for line in Lines:
    start = line.find("href='/players/playerpage/")
    # print(start)
    if start >= 0:
        # start = line.find('/players/playerpage/')
        end = line.find('</a>', start)
        text = line[int(start):int(end)]
        # print(text)
        startOfPlayerId = text.rfind('/') + 1
        endOfPlayerId = text.rfind('\'>')
        startOfPlayerName = text.rfind('\'>') + 2
        playerName = text[startOfPlayerName:]
        playerId= text[startOfPlayerId:endOfPlayerId]
        # print(":" + playerName + ":" + playerId + ":")
        # if playerId.find('\'') >= 0:
        #     playerId = playerId[0:playerId.find('\'')]
            
        startOfPositions = line.find('</span> </td><td align="right">')
        if startOfPositions < 0:
            startOfPositions = line.find('</span></td><td align="right">')
        positionText = line[startOfPositions:]
        startOfPositions = positionText.find("\">")
        #print(startOfPositions)
        startOfPositions += 2
        positionText = positionText[startOfPositions:]
        #print(positionText)
        endOfPositions = positionText.find('/td>') - 1
        positions = positionText[:endOfPositions]
        positions = positions.replace(",", "|")
        # print(positions)
        #print(startOfPositions)
        #print(endOfPositions)
        #print ("--------")
        player = next((item for item in player_id_map if item["CBSID"] == playerId), False)
        if player != False:
            # print("found!")
            fangraphsID = player["IDFANGRAPHS"]
            mlbId = player["MLBID"]
            output.writelines(playerName + ", " + playerId + ", " + fangraphsID + ", " + mlbId + ", " + positions + "|B\n")
        else:
            # print("CBSID Not Found: " + playerName + " - " + playerId)
            fangraphsID = "None"
            output2.writelines(playerName + ", " + playerId + ", " + fangraphsID + ", H, " + positions + "\n")
            
        # print(playerName + ", " + playerId + ", " + fangraphsID + ", H, " + positions)
        
output.close()
output2.close()
