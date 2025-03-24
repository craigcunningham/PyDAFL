#steps for loading players and rosters for draft
1. Download a new player id map (https://www.smartfantasybaseball.com/tools/) - (https://www.smartfantasybaseball.com/PLAYERIDMAPCSV)
1. Go to: https://dafl.baseball.cbssports.com/stats/stats-main/all:C:1B:2B:3B:SS:OF:U:P/period-1:p/All+Batters+with+Eligibility?print_rows=9999
2. Make sure it shows all players. 
3. Save as 'Webpage, HTML Only' datafiles\Rosters.html
4. Run: python .\ExtractCBSPlayers.py
5. activate the python env in PyDAFL\.venv and Run: python .\load_players.py
6. Go to: https://dafl.baseball.cbssports.com/stats/stats-main/team:all/period-1:p/MLB+Salaries
7. Save as 'Webpage, HTML Only' datafiles\AllPlayersEligibility.html
8. Run: python .\ExtractCBSRostersToRoster.py
9. Look into Shohei Otani. Did he get imported?
9. Run: python .\ExtractCBSRostersToRoster.py
10. Run: python .\load_rosters.py 


Loading player stats/value/adp
Download: https://nfc.shgn.com/adp/baseball
Select dates (last two weeks?)
It saves as a tsv file. Open it in Excel and save as csv: nfbc-adp.csv
Download: https://www.fangraphs.com/projections?pos=all&stats=bat (Select the projection system. Default is Steamer)
Save as: hitter_stats.csv
Download: https://www.fangraphs.com/projections?stats=pit (Select the projection system. Default is Steamer)
Save as: pitcher_stats.csv
Download fangraphs auction calculator for hitters.
Save as: hitters_values.csv
Download fangraphs auction calculator for pitchers.
Save as: pitchers_values.csv
Run: python load_player_values.py
Can be rerun with new data whenever
