#steps for loading players and rosters for draft
1. Download a new player id map (https://www.smartfantasybaseball.com/tools/) - (https://www.smartfantasybaseball.com/PLAYERIDMAPCSV)
1. Go to: https://dafl.baseball.cbssports.com/stats/stats-main/all:C:1B:2B:3B:SS:OF:U:P/period-1:p/All+Batters+with+Eligibility?print_rows=9999
2. Make sure it shows all players. 
3. Save as 'Webpage, HTML Only' datafiles\AllPlayersEligibility.html ?(2026 - swapped filename with #7)
4. Run: python .\ExtractCBSPlayers.py
5. activate the python env in PyDAFL\.venv and Run: python .\load_players.py
6. Go to: https://dafl.baseball.cbssports.com/stats/stats-main/team:all/period-1:p/MLB+Salaries
7. Save as 'Webpage, HTML Only' datafiles\Rosters.html ?(2026 - swapped filename with #3)
8. Run: python .\ExtractCBSRostersToRoster.py
9. Look into Shohei Otani. Did he get imported?
9. Run: python .\ExtractCBSRostersToRoster.py
10. Run: python .\load_rosters.py 


Loading player stats/value/adp
Download: https://nfc.shgn.com/adp/baseball
Select dates (last two weeks?)
It saves as a tsv file. Open it in Excel and save as csv: nfbc-adp.csv
Download: https://www.fangraphs.com/projections?pos=all&stats=bat (Select the projection system. Default is Steamer)
Save as: hitter_proj.csv
Download: https://www.fangraphs.com/projections?stats=pit (Select the projection system. Default is Steamer)
Save as: pitcher_proj.csv
Export (verify H and AB are included): https://www.fangraphs.com/leaders/major-league?pos=all&stats=bat&lg=all&qual=y&type=c%2C4%2C6%2C11%2C12%2C13%2C21%2C-1%2C34%2C35%2C40%2C41%2C-1%2C23%2C37%2C38%2C50%2C317%2C61%2C-1%2C111%2C-1%2C203%2C199%2C58%2C5%2C7&season=2026&month=0&season1=2026&ind=0&v_cr=202301
Save as: hitter_stats.csv
Export (verify ER, Holds, and SO are included): https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&lg=all&qual=y&type=c%2C4%2C5%2C11%2C7%2C8%2C13%2C-1%2C36%2C37%2C40%2C43%2C44%2C48%2C51%2C-1%2C240%2C-1%2C6%2C332%2C45%2C62%2C-1%2C59%2C17%2C114%2C24&season=2026&season1=2026&ind=0&month=0&v_cr=202301
Save as: pitcher_stats.csv
Do popup and copy to file named razzball_player_rater.csv: https://razzball.com/playerrater-mlb14team/
Download fangraphs auction calculator for hitters.
Save as: hitters_values.csv
Download fangraphs auction calculator for pitchers.
Save as: pitchers_values.csv
Run: python load_player_values.py (It can be done before or after entering protection lists, but it hasn't been tested before they are added)
Can be rerun with new data whenever
