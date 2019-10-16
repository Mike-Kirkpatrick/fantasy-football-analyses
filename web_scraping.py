#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 19:24:06 2019

@author: mike
"""

leagueId = '392495'
seasons = ['2011','2012','2013','2014','2015','2016','2017','2018']
season = '2017'

from bs4 import BeautifulSoup
import requests

def getWebpageData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


#~~~~~~~~~~~~~~~~~~~~~#
#     Team Owners     #
#~~~~~~~~~~~~~~~~~~~~~#
url = 'https://fantasy.nfl.com/league/{}/history/{}/owners'.format(leagueId,season)
soup = getWebpageData(url)

teamOwners = []
data = soup.find_all('td', class_ = 'teamOwnerName')
for datum in data:
    teamOwners.append(datum.text)

teamNames = []
data = soup.find_all('td', class_ = 'teamImageAndName')
for datum in data:
    teamNames.append(datum.text[1:]) #remove leading blank character

teamTransactions = []
data = soup.find_all('td', class_ = 'teamTransactionCount numeric')
for datum in data:
    teamTransactions.append(int(datum.text))

teamTrades = []
data = soup.find_all('td', class_ = 'teamTradeCount numeric')
for datum in data:
    teamTrades.append(int(datum.text))



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Team Standings - Regular Season     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
url = 'https://fantasy.nfl.com/league/{}/history/{}/standings?historyStandingsType=regular'.format(leagueId,season)
soup = getWebpageData(url)

standingsTeamRank = []
data = soup.find_all('td', class_ = 'teamRank first')
rank = 0
for datum in data:
    # for some reason NFL returns rank values like '6-2'
    rank = rank + 1
    standingsTeamRank.append(rank)

standingsTeamNames = []
data = soup.find_all('td', class_ = 'teamImageAndName')
for datum in data:
    standingsTeamNames.append(datum.text[1:]) #remove leading blank character

standingsTeamRecord = []
data = soup.find_all('td', class_ = 'teamRecord numeric')
for datum in data:
    standingsTeamRecord.append(datum.text)

standingsTeamWinPct = []
data = soup.find_all('td', class_ = 'teamWinPct numeric')
for datum in data:
    standingsTeamWinPct.append(float(datum.text))

standingsTeamPointsFor = []
data = soup.find_all('td', class_ = 'teamPts stat numeric')
for datum in data:
    standingsTeamPointsFor.append(float(datum.text.replace(',','')))

standingsTeamPointsAgainst = []
data = soup.find_all('td', class_ = 'teamPts stat numeric last')
for datum in data:
    standingsTeamPointsAgainst.append(float(datum.text.replace(',','')))


#~~~~~~~~~~~~~~~~~~#
#     SCHEDULE     #
#~~~~~~~~~~~~~~~~~~#
# FIRST GET THE SCHEDULE - THEN ITERATE THRU EACH 12 OF THE PRIMARY teadId of the gameCenter
url = 'https://fantasy.nfl.com/league/392495/history/2018/schedule'


#~~~~~~~~~~~~~~~~~~~~~#
#     Game Center     #
#~~~~~~~~~~~~~~~~~~~~~#
season = 2011
teamId = 1
week = 13

url = 'https://fantasy.nfl.com/league/392495/history/{}/teamgamecenter?teamId={}&week={}'.format(season,teamId,week)
soup = getWebpageData(url)

playerPosition = []
data = soup.find_all('td', class_ = 'teamPosition')
for datum in data:
    playerPosition.append(datum.text)

playerNameAndInfo = []
data = soup.find_all('td', class_ = 'playerNameAndInfo')
for datum in data:
    playerNameAndInfo.append(datum.text)

playerOpponent = []
data = soup.find_all('td', class_ = 'playerOpponent')
for datum in data:
    playerOpponent.append(datum.text)

playerGameStatus = []
data = soup.find_all('td', class_ = 'playerGameStatus')
for datum in data:
    playerGameStatus.append(datum.text)

playerPoints = []
data = soup.find_all('span', class_ = 'playerTotal')
for datum in data:
    playerPoints.append(datum.text)

# Don't really need. Can sum points for non "BN" positions
teamPoints = []
data = soup.find_all('span', class_ = 'teamTotal teamId-1')
for datum in data:
    teamPoints.append(datum.text)

teamName = []
data = soup.find_all('span', class_ = 'teamTotal teamId-1')
data = soup.find_all('span', class_ = 'teamTotal')
for datum in data:
    teamPoints.append(datum.text)



#~~~~~~~~~~~~~~~~~#
url = 'https://fantasy.nfl.com/league/392495/history/2017/teamgamecenter?teamId=5&week=8'


url = 'https://fantasy.nfl.com/league/392495/history/2017/teamhome?teamId=11'
soup = getWebpageData(url)

owner_name = soup.find_all('ul', class_ = 'owners')[0].text
owner_name = soup.find_all('ul', class_ = 'owners')[0].text

teamStats = owner_name = soup.find_all('ul', class_ = 'teamStats')
place = teamStats[1].text.replace('Season Result ','').replace(' Place','').replace('st','').replace('nd', '').replace('rd', '').replace('th', '')

teamStats[1].text.replace('Rank ','')

Rank 1Record 10-3-0Streak W1

teamStats[1].text.replace('Season Result ', '').replace(' Place', '')
t.text.replace('Season Result ', '').replace(' Place', '')

owner_info = []
owner_info_data = soup.find_all('ul', class_ = 'owners')
owner_info_data = soup.find_all('ul', class_ = 'owners')[0].text
for owner in owner_info_data:
    owner_info.append(owner.text)
print(owner_info_data)
print(owner_info)

# Get each individual teams data. Team name, teamId, and owner name
# Get final standing, total points, regular season record
https://fantasy.nfl.com/league/392495/history/2017/teamhome?teamId=5


player_info = []
player_info_data = soup.find_all('td', class_ = 'playerNameAndInfo')
for player_inf in player_info_data:
    player_info.append(player_inf.text)

# 0-15 are team 1, 16-31 are team 2
player_points = []
points_data = soup.find_all('td', class_ = 'stat statTotal numeric last')
for point in points_data:
    player_points.append(point.text.strip())

player_opponents = []
player_opponents_data = soup.find_all('td', class_ = 'playerOpponent')
for player_opponent in player_opponents_data:
    player_opponents.append(player_opponent.text)


divs = soup.find_all('td', class_ = 'playerOpponent')
for div in divs:
    print(div.text.strip())
    print(div.text)
print(soup.prettify())

#tableWrapBN-1

#teamMatchupSecondary
.teamWrap-1
.last

.playerId-2555259

adjustedPts

divs = soup.find_all('div', class_ = 'lister-item mode-advanced')
divs = soup.find_all('div')
divs = soup.find_all('table')
divs = soup.find_all('td', class_ = 'playerNameAndInfo')
divs = soup.find_all('td')
print(len(divs))
print(divs)

for div in divs:
    print(div)

<td class="playerNameAndInfo" id="yui_3_15_0_1_1571020570002_714"><div class="c c-phi" id="yui_3_15_0_1_1571020570002_715"><b></b><a onclick="s_objectID=&quot;https://fantasy.nfl.com/players/cardhistory?gameSeason=2017&amp;leagueId=392495&amp;playerId=2555259_1&quot;;return this.s_oc?this.s_oc(e):true" href="/players/cardhistory?gameSeason=2017&amp;leagueId=392495&amp;playerId=2555259" class="playerCard playerName playerNameFirstInitialLastName playerNameId-2555259 what-playerCard" id="yui_3_15_0_1_1571020570002_805">C. Wentz</a> <em id="yui_3_15_0_1_1571020570002_716">QB - PHI</em>    </div></td>

#yui_3_15_0_1_1571020570002_598


#yui_3_15_0_1_1571020570002_598

#yui_3_15_0_1_1571020570002_597
print(soup.yui_3_15_0_1_1571020570002_597)

soup.findChildren

//*[@id="yui_3_15_0_1_1571020570002_597"]

soup.cdata_list_attributes
soup.name
print(soup.body.div)
print(soup.children)

for c in soup.children:
    print(c)


print(soup.doc)
soup.text
print(soup.html.body)
print(soup)
print(soup.attrs)
print(soup.body.div.div.div.div)

soup.select('#yui_3_15_0_1_1571020570002_598')

/html/body/div[2]/div[3]/div/div[1]/div/div[5]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/table/tbody/tr[1]/td[7]/span




