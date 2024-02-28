#steps for loading players and rosters for draft
1. Go to: https://dafl.baseball.cbssports.com/stats/stats-main/all:C:1B:2B:3B:SS:OF:U:P/period-1:p/All+Batters+with+Eligibility?print_rows=9999
2. Make sure it shows all players. 
3. Save as 'Webpage, HTML Only'
4. Run: python .\ExtractCBSPlayers.py
5. Run: python .\load_players.py
6. Go to: https://dafl.baseball.cbssports.com/stats/stats-main/team:all/period-1:p/MLB+Salaries
7. Save as 'Webpage, HTML Only'
8. Run: python .\ExtractCBSRostersToRoster.py
9. Look into Shohei Otani. Did he get imported?
9. Run: python .\ExtractCBSRostersToRoster.py
10. Run: python .\load_rosters.py 
11. Download nfbc adp - https://nfc.shgn.com/adp/baseball - 15 teams, draft champions, last 14 or 30 days? - nfbc-adp.csv
12. Dowload hitter and pitcher values from auction calculator. hitters_values.csv and pitchers_values.csv
13. Download stats from fangraphs: hitter_stats.csv and pitcher_stats.csv
14. Run: python .\load_player_values.py
