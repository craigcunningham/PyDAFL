from csv import DictReader

def GetTeam(line):
	startOfTeam = line.find("'/teams/")+8
	endOfTeam = line.find("'>", startOfTeam)
	team = line[startOfTeam:endOfTeam]
	#Convert CBS Team to DAFL Team
	if team == "16":
		team = 6
	elif team == "5":
		team = 7
	elif team == "11":
		team = 8
	elif team == "13":
		team = 9
	elif team == "9":
		team = 10
	elif team == "6":
		team = 11
	elif team == "16":
		team = 12
	elif team == "10":
		team = 13
	elif team == "14":
		team = 14
	elif team == "12":
		team = 15
	elif team == "15":
		team = 16
	elif team == "3":
		team = 17
	elif team == "17":
		team = 18
	
	return team

def ExtractText(start, line):
	#print(start)
	startOfData = line.find("\">", start)
	#print(startOfData)
	startOfData += 2
	endOfData = line.find('/td>', startOfData) - 1
	data = line[startOfData:endOfData]
	#print(endOfData)
	return data, endOfData

with open("./datafiles/player_id_map.csv", 'r') as f:
    dict_reader = DictReader(f)
    player_id_map = list(dict_reader)
# output = open("./datafiles/rosters.csv", "w")
output2 = open("./datafiles/rosteredplayers.csv", "w")
# output.writelines("team_id,name,cbs_id,eligible,old_salary,old_contract,new_salary,new_contract,protect,playerid\n")
fileName = "./datafiles/Rosters.html"
with open(fileName, "rt") as file:
    Lines = file.readlines()

for line in Lines:
	team = GetTeam(line)
	# print(team)
	start = line.find('href=\'/players/playerpage/')
	end = line.find('</a>', start)
	text = line[int(start):int(end)]
	startOfPlayerId = text.rfind('/') + 1
	endOfPlayerId = text.rfind('\'')
	startOfPlayerName = text.rfind('>') + 1
	playerName = text[startOfPlayerName:]
	playerId= text[startOfPlayerId:endOfPlayerId]
	if playerId.find('\'') >= 0:
		playerId = playerId[0:playerId.find('\'')]
	# print(playerId)
	startOfActiveInactive = line.find('</span> </td><td align="right">')
	if startOfActiveInactive < 0:
		startOfActiveInactive = line.find('</span></td><td align="right">')
	startOfPositions = line.find('</td><td align="right">', startOfActiveInactive+10)
	if startOfPositions > 0:
		positions, nextStart = ExtractText(startOfPositions, line)
		positions = positions.replace(",", "|")

		startOfSalary = line.find('<td align="right">', nextStart)
		if startOfSalary < 0:
			startOfSalary = line.find('<td align="right">')
		if startOfSalary > 0:
			salary, nextStart = ExtractText(startOfSalary, line)
			
		startOfContractYear = line.find('<td align="right">', nextStart)
		if startOfContractYear < 0:
			startOfContractYear = line.find('<td align="right">')
		if startOfContractYear > 0:
			contractYear, nextStart = ExtractText(startOfContractYear, line)
		
		contractYearNew = int(contractYear)+1
		salaryNew = int(salary)
		if contractYearNew > 2:
			salaryNew = int(salary) + ((int(contractYearNew)-2)*5)		
	# print(playerName)
	if playerName != "":
		player = next((item for item in player_id_map if item["CBSID"] == playerId), False)
		if player != False:
			fangraphsID = player["IDFANGRAPHS"]
			mlbId = player["MLBID"]
			output2.writelines(playerName + ", " + playerId + ", " + fangraphsID + ", " + mlbId + ", " + positions + "\n")
		# output.writelines(str(team) + ", \"" + playerName + "\", " + playerId + ", \"" + positions + "\"" + ", \"" + str(salary) + "\"" + ", \"" + str(contractYear) + "\", \"" + str(salaryNew) + "\"" + ", \"" + str(contractYearNew) + "\", \"0\", \"0\"\n")
        
# output.close()
output2.close()
