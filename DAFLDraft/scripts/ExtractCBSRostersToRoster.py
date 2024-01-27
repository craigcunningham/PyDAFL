your_djangoproject_home="C:../../"
import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='web_project.settings'

import django
django.setup()
from DAFLDraft.models import Player

from csv import DictReader


def GetTeam(line):
	startOfTeam = line.find("'/teams/")+8
	endOfTeam = line.find("'>", startOfTeam)
	team = line[startOfTeam:endOfTeam]
	#Convert CBS Team to DAFL Team
	if team == "1":
		team = 1
	elif team == "2":
		team = 2
	elif team == "3":
		team = 3
	elif team == "5":
		team = 9
	elif team == "6":
		team = 4
	elif team == "9":
		team = 6
	elif team == "10":
		team = 12
	elif team == "11":
		team = 10
	elif team == "12":
		team = 11
	elif team == "13":
		team = 14
	elif team == "14":
		team = 5
	elif team == "15":
		team = 8
	if team == "16":
		team = 13
	elif team == "17":
		team = 7
	
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

with open("./datafiles/player_id_map.csv", 'r', encoding='utf-8') as f:
    dict_reader = DictReader(f)
    player_id_map = list(dict_reader)
    
output = open("./datafiles/rosters.csv", "w", encoding='utf-8')
output2 = open("./datafiles/cbsid_notfound.csv", "w", encoding='utf-8')
# output.writelines("team_id,name,cbs_id,eligible,old_salary,old_contract,new_salary,new_contract,protect,playerid\n")
fileName = "./datafiles/Rosters.html"
with open(fileName, "rt") as file:
    Lines = file.readlines()

for line in Lines:
	start = line.find('href=\'/players/playerpage/')
	if start > 0:
		team = GetTeam(line)
		end = line.find('</a>', start)
		text = line[int(start):int(end)]
		startOfPlayerId = text.rfind('/') + 1
		endOfPlayerId = text.rfind('\'>')
		startOfPlayerName = text.rfind('>') + 1
		playerName = text[startOfPlayerName:]
		playerId= text[startOfPlayerId:endOfPlayerId]
		if playerId.find('\'') >= 0:
			playerId = playerId[0:playerId.find('\'')]
		if playerId.find('?') >= 0:
			playerId = playerId[0:playerId.find('?')]
			
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

			if playerName != "":
				daflPlayer = Player.objects.all().filter(cbs_id = playerId).first()
				if daflPlayer:
					# team, player_id, position, new_salary, new_contract_year, active
					if positions.find("|") > 0:
						position = positions[0: positions.find("|")].strip()
					else:
						position = positions.strip()
					output.writelines(str(team) + ", " + str(daflPlayer.id) + ", " + position + ", " + str(salaryNew) + ", " + str(contractYearNew) + ", 0\n")
					#output.writelines(str(team) + ", \"" + playerName + "\", " + str(daflPlayer.id) + ", \"" + positions + "\"" + ", \"" + str(salary) + "\"" + ", \"" + str(contractYear) + "\", \"" + str(salaryNew) + "\"" + ", \"" + str(contractYearNew) + "\", \"0\", \"0\"\n")
				else:
					output2.writelines(playerId)
        
output.close()
output2.close()