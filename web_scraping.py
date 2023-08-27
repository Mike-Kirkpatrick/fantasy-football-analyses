#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 19:24:06 2019

@author: mike
"""

# Set the working directory to wherever the repository was cloned to
from os import chdir
chdir('/home/mike/fantasy-football-analyses')

# Get leagueId
# Login to your league via https://fantasy.nfl.com
# Your leagueId is not in the url as such https://fantasy.nfl.com/league/392495
leagueId = '392495'


from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime as dt
import time

def getWebpageData(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Seasons-Weeks-TeamIds Dictionary     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# We create a dictionary with all the season, weeks and teamIds.
# Our weeks and teamIds have changed over the seasons.
# Some seasons have 16 weeks and some have 17.
# Starting in season 2017, we swapped out teamId=10 for teamId=13
# In 2021, Matt Smith came back as teamId=14

sixteenWeeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
seventeenWeeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
standardTeamIds = [1,2,3,4,5,6,7,8,9,10,11,12]
teamIdsNo10 = [1,2,3,4,5,6,7,8,9,11,12,13]
teamIds2021 = [1,2,3,4,5,6,7,8,9,11,13,14]

seasonsWeeksTeamIds = {
	2011:{
       'Weeks': seventeenWeeks,
       'TeamIds': standardTeamIds
	},
	2012:{
       'Weeks': seventeenWeeks,
       'TeamIds': standardTeamIds
	},
	2013:{
       'Weeks': sixteenWeeks,
       'TeamIds': standardTeamIds
	},
	2014:{
       'Weeks': sixteenWeeks,
       'TeamIds': standardTeamIds
	},
	2015:{
       'Weeks': sixteenWeeks,
       'TeamIds': standardTeamIds
	},
	2016:{
       'Weeks': sixteenWeeks,
       'TeamIds': standardTeamIds
	},
	2017:{
       'Weeks': sixteenWeeks,
       'TeamIds': teamIdsNo10
	},
	2018:{
       'Weeks': sixteenWeeks,
       'TeamIds': teamIdsNo10
	},
	2019:{
       'Weeks': sixteenWeeks,
       'TeamIds': teamIdsNo10
	},
	2020:{
       'Weeks': sixteenWeeks,
       'TeamIds': teamIdsNo10
	},
	2021:{
       'Weeks': seventeenWeeks,
       'TeamIds': teamIds2021
	},
	2022:{
       'Weeks': seventeenWeeks,
       'TeamIds': teamIds2021
	},
}

del sixteenWeeks, seventeenWeeks, standardTeamIds, teamIdsNo10

#~~~~~~~~~~~~~~~~~~~~~#
#     Team Owners     #
#~~~~~~~~~~~~~~~~~~~~~#
def getTeamOwners():
    teamOwnersDf = pd.DataFrame()
    for season in seasonsWeeksTeamIds:
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
        
        ownersList =  list(zip(teamOwners, teamNames, teamTransactions, teamTrades))
        ownersDfSeason = pd.DataFrame(ownersList, columns = ['teamOwner', 'teamName', 'teamTransactions', 'teamTrades']) 
        ownersDfSeason['season'] = season
        teamOwnersDf = pd.concat([teamOwnersDf, ownersDfSeason], axis=0)
    return teamOwnersDf

teamOwners = getTeamOwners()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Team Standings - Regular Season     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def regularSeason():
    df = pd.DataFrame()
    for season in seasonsWeeksTeamIds:
        url = 'https://fantasy.nfl.com/league/{}/history/{}/standings?historyStandingsType=regular'.format(leagueId,season)
        soup = getWebpageData(url)
        
        teamNames = []
        data = soup.find_all('td', class_ = 'teamImageAndName')
        for datum in data:
            teamNames.append(datum.text[1:]) #remove leading blank character
        
        teamRank = []
        data = soup.find_all('td', class_ = 'teamRank first')
        rank = 0
        for datum in data:
            # for some reason NFL returns rank values like '6-2'
            rank = rank + 1
            teamRank.append(rank)
        
        teamRecord = []
        data = soup.find_all('td', class_ = 'teamRecord numeric')
        for datum in data:
            teamRecord.append(datum.text)
        
        teamWinPct = []
        data = soup.find_all('td', class_ = 'teamWinPct numeric')
        for datum in data:
            teamWinPct.append(float(datum.text))
        
        teamPointsFor = []
        data = soup.find_all('td', class_ = 'teamPts stat numeric')
        for datum in data:
            teamPointsFor.append(float(datum.text.replace(',','')))
        
        teamPointsAgainst = []
        data = soup.find_all('td', class_ = 'teamPts stat numeric last')
        for datum in data:
            teamPointsAgainst.append(float(datum.text.replace(',','')))
        
        List =  list(zip(teamNames, teamRank, teamRecord, teamWinPct, teamPointsFor, teamPointsAgainst))
        seasonDf = pd.DataFrame(List, columns = ['teamName', 'teamRankRegSeason', 'teamRecordRegSeason', 'teamWinPctRegSeason', 'teamPointsForRegSeason', 'teamPointsAgainstRegSeason']) 
        seasonDf['season'] = season
        df = pd.concat([df, seasonDf], axis=0)
    return df

regularSeason = regularSeason()



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Team Standings - Final     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def finalStandings():
    df = pd.DataFrame()
    for season in seasonsWeeksTeamIds:
        url = 'https://fantasy.nfl.com/league/{}/history/{}/standings'.format(leagueId,season)
        soup = getWebpageData(url)
        
        teamNames = []
        data = soup.find_all('a', class_ = 'teamName')
        for datum in data:
            teamNames.append(datum.text)
        teamNames = teamNames[1:] #it lists the champion twice
        
        teamFinalStandings = []
        data = soup.find_all('div', class_ = 'place')
        for datum in data:
            teamFinalStandings.append(int(datum.text.replace(' Place','').replace('st','').replace('nd','').replace('rd','').replace('th','')))
        
        
        List =  list(zip(teamNames, teamFinalStandings))
        seasonDf = pd.DataFrame(List, columns = ['teamName', 'teamFinalStanding']) 
        seasonDf['season'] = season
        df = pd.concat([df, seasonDf], axis=0)
    return df

finalStandings = finalStandings()

#~~~~~~~~~~~~~~~~~~~~~~#
#     OWNER-SEASON     #
#~~~~~~~~~~~~~~~~~~~~~~#
ownerSeason = pd.merge(teamOwners, regularSeason, on=['teamName', 'season'])
ownerSeason = pd.merge(ownerSeason, finalStandings, on=['teamName', 'season'])

ownerSeason.to_csv('data/raw_data_owner_season.csv', index=False)

#~~~~~~~~~~~~~~~~~~#
#     MATCHUPS     #
#~~~~~~~~~~~~~~~~~~#
def winLoss(row):
    if row['teamWeekTotal'] > row['teamWeekTotalOpponent']:
        result = 'Win'
    elif row['teamWeekTotal'] < row['teamWeekTotalOpponent']:
        result = 'Loss'
    elif row['teamWeekTotal'] == row['teamWeekTotalOpponent']:
        result = 'Tie'
    return result

def getMatchupsWeek(season, week):
    url = 'https://fantasy.nfl.com/league/{l}/history/{s}/schedule?gameSeason={s}&leagueId={l}&scheduleDetail={w}&scheduleType=week&standingsTab=schedule'.format_map({'l':leagueId, 's':season, 'w':week})
    soup = getWebpageData(url)
    
    teamOwner = []
    data = soup.find_all('li', class_ = 'name')
    for datum in data:
        teamOwner.append(datum.text)
    
    teamName = []
    data = soup.find_all('a', class_ = 'teamName')
    for datum in data:
        teamName.append(datum.text)
    
    teamTotal = []
    data = soup.find_all('div', class_ = 'teamTotal')
    for datum in data:
        teamTotal.append(float(datum.text))
    
    teamRecord = []
    data = soup.find_all('span', class_ = 'teamRecord')
    for datum in data:
        teamRecord.append(datum.text)
    
    teamOwner1 = teamOwner[0::2]
    teamOwner2 = teamOwner[1::2]
    teamName1 = teamName[0::2]
    teamName2 = teamName[1::2]
    teamTotal1 = teamTotal[0::2]
    teamTotal2 = teamTotal[1::2]
    teamRecord1 = teamRecord[0::2]
    teamRecord2 = teamRecord[1::2]
    
    matchupsList1 =  list(zip(teamOwner1, teamName1, teamTotal1, teamRecord1, teamOwner2, teamName2, teamTotal2, teamRecord2))
    matchupsDf1 = pd.DataFrame(matchupsList1, columns = ['teamOwner', 'teamName', 'teamWeekTotal', 'teamRecordPost', 'teamOwnerOpponent', 'teamNameOpponent', 'teamWeekTotalOpponent', 'teamRecordPostOpponent']) 
    matchupsList2 =  list(zip(teamOwner2, teamName2, teamTotal2, teamRecord2, teamOwner1, teamName1, teamTotal1, teamRecord1))
    matchupsDf2 = pd.DataFrame(matchupsList2, columns = ['teamOwner', 'teamName', 'teamWeekTotal', 'teamRecordPost', 'teamOwnerOpponent', 'teamNameOpponent', 'teamWeekTotalOpponent', 'teamRecordPostOpponent']) 
    matchupsDf = pd.concat([matchupsDf1, matchupsDf2], axis=0)
    matchupsDf['season'] = season
    matchupsDf['week'] = week
    matchupsDf['teamMatchupResult'] = matchupsDf.apply(winLoss, axis=1)
    return matchupsDf

def getMatchups():
    matchups = pd.DataFrame()
    for season in seasonsWeeksTeamIds:
        for week in seasonsWeeksTeamIds[season]['Weeks']:
            matchupsWeek = getMatchupsWeek(season, week)
            matchups = pd.concat([matchups, matchupsWeek], axis=0)
    matchups['teamRecordPre'] = matchups.groupby(['teamOwner', 'teamName', 'season'])['teamRecordPost'].shift(1)
    matchups.teamRecordPre.loc[matchups['week'] == 1] = '0-0-0'
    matchups['teamRecordPreOpponent'] = matchups.groupby(['teamOwnerOpponent', 'teamNameOpponent', 'season'])['teamRecordPostOpponent'].shift(1)
    matchups.teamRecordPreOpponent.loc[matchups['week'] == 1] = '0-0-0'
    matchups = matchups.reset_index()
    matchups['teamWeekRank'] = matchups.sort_values(['season','week','teamWeekTotal'], ascending=[True, True,False]) \
        .groupby(['season','week']) \
        .cumcount() + 1
    matchups['teamWeekRankOpponent'] = matchups.sort_values(['season','week','teamWeekTotalOpponent'], ascending=[True, True,False]) \
        .groupby(['season','week']) \
        .cumcount() + 1
    # reorder columns
    matchups = matchups[['season', 'week', 'teamOwner', 'teamName', 'teamWeekTotal', 'teamWeekRank', 'teamRecordPre', 'teamMatchupResult', 'teamRecordPost', 'teamOwnerOpponent', 'teamNameOpponent', 'teamWeekTotalOpponent', 'teamWeekRankOpponent', 'teamRecordPreOpponent', 'teamRecordPostOpponent']]
    return matchups

             
matchups = getMatchups()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     OWNER-SEASON-WEEK     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
matchups.to_csv('data/raw_data_owner_season_week.csv', index=False)



#~~~~~~~~~~~~~~~~~~~~~#
#     Game Center     #
#~~~~~~~~~~~~~~~~~~~~~#
def gameCenter():
    '''
    This page gives us data for both teams.
    We only want team 1, so we cut the data in half for each iteration
    This one takes a little while to finish - Almost 2 mins per season
    '''
    start_time = time.time()
    finalDf = pd.DataFrame()
    for season in seasonsWeeksTeamIds:
        for week in seasonsWeeksTeamIds[season]['Weeks']:
            for teamId in seasonsWeeksTeamIds[season]['TeamIds']:
                #print('Season:', season, 'Week:', week, 'TeamId:', teamId)
                url = 'https://fantasy.nfl.com/league/392495/history/{}/teamgamecenter?teamId={}&week={}'.format(season,teamId,week)
                soup = getWebpageData(url)
                
                teamName = []
                data = soup.find_all('a', class_ = 'teamName')
                for datum in data:
                    teamName.append(datum.text)
                teamName = teamName[0]
                
                # In between the 2022 and 2023 season the userName code
                # stopped working. I inspected the webpage and can see that userName
                # is there, but for some reason beautiful soup can't get it.
                # Instead of searching thru nasty html, I'm just going to subset
                # the ownerSeason DF to get Owner.
                teamOwner = teamOwners[(teamOwners["teamName"]==teamName) & (teamOwners["season"]==season)]["teamOwner"].iloc[0]
                # Old code
                #teamOwner = []
                #data = soup.find_all('a', class_ = 'userName')
                #for datum in data:
                #    teamOwner.append(datum.text)
                #teamOwner = teamOwner[0]
                
                teamPoints = []
                data = soup.find_all('span', class_ = 'teamTotal teamId-{}'.format(teamId))
                for datum in data:
                    #teamPoints.append(float(datum.text))
                    teamPoints.append(datum.text)
                teamPoints = teamPoints[0]
                
                playerRosterPosition = []
                data = soup.find_all('td', class_ = 'teamPosition')
                for datum in data:
                    playerRosterPosition.append(datum.text)
                playerRosterPosition = playerRosterPosition[0:16]                
                
                playerNameAndInfo = []
                data = soup.find_all('td', class_ = 'playerNameAndInfo')
                for datum in data:
                    playerNameAndInfo.append(datum.text)
                playerNameAndInfo = playerNameAndInfo[0:16]
                    
                playerOpponent = []
                data = soup.find_all('td', class_ = 'playerOpponent')
                for datum in data:
                    playerOpponent.append(datum.text)
                playerOpponent = playerOpponent[0:16]
                
                playerGameStatus = []
                data = soup.find_all('td', class_ = 'playerGameStatus')
                for datum in data:
                    playerGameStatus.append(datum.text)
                playerGameStatus = playerGameStatus[0:16]
                
                playerPoints = []
                data = soup.find_all('td', class_ = 'statTotal')
                for datum in data:
                    playerPoints.append(datum.text)
                playerPoints = playerPoints[0:16]
                
                ls =  list(zip(playerRosterPosition, playerNameAndInfo, playerPoints, playerOpponent, playerGameStatus))
                df = pd.DataFrame(ls, columns = ['playerRosterPosition', 'playerNameAndInfo', 'playerPoints', 'playerOpponent', 'playerGameStatus'])
                df.insert(0, 'teamPoints', teamPoints)
                df.insert(0, 'teamName', teamName)
                df.insert(0, 'teamOwner', teamOwner)
                df.insert(0, 'week', week)
                df.insert(0, 'season', season)
                finalDf = pd.concat([finalDf, df], axis=0)
    print('--- TOTAL RUN TIME = ' + str(dt.timedelta(seconds= round(time.time() - start_time,0))))
    return finalDf

gameCenterDf = gameCenter()

# Clean up numeric columns - teams on bye have points with '-'
gameCenterDf['playerPoints'] = gameCenterDf['playerPoints'].replace('-','0.0')
gameCenterDf['playerPoints'] = pd.to_numeric(gameCenterDf.playerPoints)
gameCenterDf['teamPoints'] = pd.to_numeric(gameCenterDf.teamPoints)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     OWNER-SEASON-WEEK-PLAYER     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
gameCenterDf.to_csv('data/raw_data_owner_season_week_player.csv', index=False)

