#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 22:30:03 2019

@author: mike
"""

from os import chdir
chdir('/home/mike/fantasy-football-analyses')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

osDf = pd.read_csv('data/raw_data_owner_season.csv')
oswDf = pd.read_csv('data/raw_data_owner_season_week.csv')
oswpDf = pd.read_csv('data/raw_data_owner_season_week_player.csv')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~                             ~~~~~~~~~~#
#                    PREP DATA                    #
#~~~~~~~~~~                             ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#~~~~~~~~~~~~~~~~~~~#
#     ADD COACH     #
#~~~~~~~~~~~~~~~~~~~#
def assignCoach(row):
    '''Aj is an ass and has a space after his name'''
    teamOwner = row['teamOwner']
    teamName = row['teamName']
    coach = ''
    if teamOwner == 'AJ ' or teamOwner == 'AJ':
        coach = 'Aj Crane'
    if teamOwner == 'Aaron':
        coach = 'Aaron Horwitz'
    if teamOwner == 'Alex':
        coach = 'Alex Price'
    if teamOwner == 'Brian':
        coach = 'Brian Hazel'
    if teamOwner == 'Colin':
        coach = 'Colin Rehbein'
    if teamOwner == 'Jason':
        coach = 'Jason Murphy'
    if teamOwner == 'Kameron':
        coach = 'Kameron Burt'
    if teamOwner == 'Matt' or teamOwner == 'Matt Smith':
        coach = 'Matt Smith'
    if teamOwner == 'Matthew':
        coach = 'Matt Cisneros'
    if teamOwner == 'Mike':
        if teamName == 'Mr Pig Skinner':
            coach = 'Mike Thomas'
        elif teamName == 'MrPigSkinner':
            coach = 'Mike Thomas'
        else:
            coach = 'Mike Kirkpatrick'
    if teamOwner == 'Rob':
        coach = 'Rob Manbert'
    if teamOwner == 'Sam':
        coach = 'Sam Courtney'
    if teamOwner == 'dan' or teamOwner == 'Dan':
        coach = 'Dan Tarin'
    if teamOwner == 'nathan':
        coach = 'Nathan Radolf'
    return coach

osDf['coach'] = osDf.apply(assignCoach, axis=1)
oswDf['coach'] = oswDf.apply(assignCoach, axis=1)
oswpDf['coach'] = oswpDf.apply(assignCoach, axis=1)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     ADD OPPONENT COACH     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def assignCoachOpponent(row):
    '''Aj is an ass and has a space after his name'''
    teamOwner = row['teamOwnerOpponent']
    teamName = row['teamNameOpponent']
    coach = ''
    if teamOwner == 'AJ ' or teamOwner == 'AJ':
        coach = 'Aj Crane'
    if teamOwner == 'Aaron':
        coach = 'Aaron Horwitz'
    if teamOwner == 'Alex':
        coach = 'Alex Price'
    if teamOwner == 'Brian':
        coach = 'Brian Hazel'
    if teamOwner == 'Colin':
        coach = 'Colin Rehbein'
    if teamOwner == 'Jason':
        coach = 'Jason Murphy'
    if teamOwner == 'Kameron':
        coach = 'Kameron Burt'
    if teamOwner == 'Matt' or teamOwner == 'Matt Smith':
        coach = 'Matt Smith'
    if teamOwner == 'Matthew':
        coach = 'Matt Cisneros'
    if teamOwner == 'Mike':
        if teamName == 'Mr Pig Skinner':
            coach = 'Mike Thomas'
        elif teamName == 'MrPigSkinner':
            coach = 'Mike Thomas'
        else:
            coach = 'Mike Kirkpatrick'
    if teamOwner == 'Rob':
        coach = 'Rob Manbert'
    if teamOwner == 'Sam':
        coach = 'Sam Courtney'
    if teamOwner == 'dan' or teamOwner == 'Dan':
        coach = 'Dan Tarin'
    if teamOwner == 'nathan':
        coach = 'Nathan Radolf'
    return coach

oswDf['coachOpponent'] = oswDf.apply(assignCoachOpponent, axis=1)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     ADD REGULAR SEASON WEEKS INDICATOR     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def getSeasonWeekDict(seasonDf):
    def regSeasonMaxWeek(row):
        record = row['teamRecordRegSeason']
        wks = 0
        for rec in record.split('-'):
            wks = wks + int(rec)
        return wks
    temp = pd.DataFrame(seasonDf.groupby('season')['teamRecordRegSeason'].max())
    temp['regSeasonMaxWeek'] = temp.apply(regSeasonMaxWeek, axis=1)
    seasons = list(temp.index.values)
    regSeasonMaxWeek = temp['regSeasonMaxWeek'].tolist()
    dic = dict(zip(seasons, regSeasonMaxWeek))
    return dic

def isRegSeasonWeek(row):
    wkTest = seasonWeek[row['season']]
    if row['week'] <= wkTest:
        isRegSeason = 1
    elif row['week'] > wkTest:
        isRegSeason = 0
    return isRegSeason

seasonWeek = getSeasonWeekDict(osDf)
oswDf['isRegSeason'] = oswDf.apply(isRegSeasonWeek, axis=1)
oswpDf['isRegSeason'] = oswpDf.apply(isRegSeasonWeek, axis=1)
del seasonWeek


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     ADD PLAYER POSITION     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def playerPosition(row):
    player = row['playerNameAndInfo']
    playerPosition = None
    DPs = [' LB ', ' DB ', ' DL ']
    positions = ['QB', 'RB', 'WR', 'TE', 'K']
    if player == '--empty--':
        playerPosition = 'Empty'
    elif ' DEF' in player:
        playerPosition = 'DEF'
    elif any(DP in player for DP in DPs):
        playerPosition = 'DP'
    else:
        for pos in positions:
            if ' {} '.format(pos) in player:
                playerPosition = pos
    return playerPosition

oswpDf['playerPosition'] = oswpDf.apply(playerPosition, axis=1)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     ADD SHITTY LOSSES INDICATOR     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
''' For each coach, what percent of your losses are shitty losses?
    A shitty loss is when you lose and your points are higher than 
    the median points for the week'''
def shittyLosses(row):
    matchupResult = row['teamMatchupResult']
    weekRank = row['teamWeekRank']
    regSeason = row['isRegSeason']
    if matchupResult == 'Loss' and weekRank < 7 and regSeason == 1:
        bsWin = 100
    elif matchupResult == 'Loss' and weekRank > 7 and regSeason == 1:
        bsWin = 0
    else:
        bsWin = None
    return bsWin

oswDf['shittyLoss'] = oswDf.apply(shittyLosses, axis=1)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     ADD BULLSHIT WINS INDICATOR     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
''' For each coach, what percent of your wins are bullshit wins?
    A bullshit win is when you win and your points are less than 
    the median points for the week'''
def bullshitWins(row):
    matchupResult = row['teamMatchupResult']
    weekRank = row['teamWeekRank']
    regSeason = row['isRegSeason']
    if matchupResult == 'Win' and weekRank >= 7 and regSeason == 1:
        bsWin = 100
    elif matchupResult == 'Win' and weekRank < 7 and regSeason == 1:
        bsWin = 0
    else:
        bsWin = None
    return bsWin

oswDf['bullshitWin'] = oswDf.apply(bullshitWins, axis=1)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     ADD POOR COACHING     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def poorCoaching(row):
    poorCoaching = None
    if row['playerPosition'] != 'BN' and row['isRegSeason'] == 1:
        if row['playerPoints'] <= 0.0:
            poorCoaching = 1
        elif row['playerPoints'] > 0.0:
            poorCoaching = 0
    return poorCoaching

oswpDf['poorCoaching'] = oswpDf.apply(poorCoaching, axis=1)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     ADD ACTIVE COACH INDICATOR     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def activeCoach(df):
    maxSeason = df.season.max()
    activeCoachList = df[df.season == maxSeason].coach.unique()
    def activeCoachIndicator(row):
        if row['coach'] in activeCoachList:
            isActiveCoach = 1
        else:
            isActiveCoach = 0
        return isActiveCoach
    df['isActiveCoach'] = df.apply(activeCoachIndicator, axis=1)
    return df

osDf = activeCoach(osDf)
oswDf = activeCoach(oswDf)
oswpDf = activeCoach(oswpDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     ADD ACTIVE OPPENENT COACH INDICATOR     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def activeCoachOpponent(df):
    maxSeason = df.season.max()
    activeCoachList = df[df.season == maxSeason].coach.unique()
    def activeCoachIndicator(row):
        if row['coachOpponent'] in activeCoachList:
            isActiveCoach = 1
        else:
            isActiveCoach = 0
        return isActiveCoach
    df['isActiveCoachOpponent'] = df.apply(activeCoachIndicator, axis=1)
    return df

oswDf = activeCoachOpponent(oswDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     ADD WIN INDICATOR     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def winner(row):
    if row['teamMatchupResult'] == 'Win':
        return 1
    else:
        return 0

oswDf['isWin'] = oswDf.apply(winner, axis=1)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~                         ~~~~~~~~~~#
#                    PLOTS                    #
#~~~~~~~~~~                         ~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Seasons Participated     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotSeasonsParticipated(df):
    df = df.sort_values(by=['coach'], ascending=False)
    plt.scatter(df.season, df.coach)
    plt.title('Seasons Participated')
    plt.xlabel('One dot per season participated')
    plt.savefig('plots/seasons_participated.png', dpi=200, bbox_inches='tight')
    
plotSeasonsParticipated(osDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Playoff Appearances     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotPlayoffAppearances(df):
    df = df[df.isActiveCoach ==1]
    def playoffAppearance(row):
        rank = row['teamRankRegSeason']
        if rank <= 6:
            playoff = 1
        elif rank > 6:
            playoff = 0
        return playoff
    measureLabel = 'playoffAppearance'
    df[measureLabel] = df.apply(playoffAppearance, axis=1)
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean())
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*1000)/10) + '%'
        newLabels.append(newLabel) 
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Playoff Appearances')
    plt.xlabel('Percent of seasons in which you made it to the playoffs')
    plt.savefig('plots/playoff_appearances.png', dpi=200, bbox_inches='tight')

plotPlayoffAppearances(osDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Playoff Champions     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotPlayoffChampions(df):
    df = df[df.isActiveCoach ==1]
    def playoffChampion(row):
        rank = row['teamFinalStanding']
        if rank == 1:
            champion = 1
        else:
            champion = 0
        return champion
    measureLabel = 'playoffChampion'
    df[measureLabel] = df.apply(playoffChampion, axis=1)
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean())
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*1000)/10) + '%'
        newLabels.append(newLabel) 
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Playoff Champions')
    plt.xlabel('Percent of seasons in which you were the Champion')
    plt.savefig('plots/playoff_champion.png', dpi=200, bbox_inches='tight')

plotPlayoffChampions(osDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Playoff Medalist     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotPlayoffMedalist(df):
    df = df[df.isActiveCoach ==1]
    def fn(row):
        rank = row['teamFinalStanding']
        if rank <= 3:
            medalist = 1
        else:
            medalist = 0
        return medalist
    measureLabel = 'playoffMedalist'
    df[measureLabel] = df.apply(fn, axis=1)
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean())
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*1000)/10) + '%'
        newLabels.append(newLabel) 
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Playoff Medalist')
    plt.xlabel('Percent of seasons in which you got 3rd place or better')
    plt.savefig('plots/playoff_medalist.png', dpi=200, bbox_inches='tight')

plotPlayoffMedalist(osDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Trades     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonAvgTrades(df):
    df = df[df.isActiveCoach ==1]
    measureLabel = 'teamTrades'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean())
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*10)/10)
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Regular Season Trades')
    plt.xlabel('Average number of trades during regular season')
    plt.savefig('plots/reg_season_trades.png', dpi=200, bbox_inches='tight')

plotRegSeasonAvgTrades(osDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Transactions     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonAvgTransactions(df):
    df = df[df.isActiveCoach ==1]
    pltTitle = 'Regular Season Transactions'
    pltXLabel = 'Average number of transactions (pickups) during regular season'
    pltFile = 'plots/reg_season_transactions.png'
    measureLabel = 'teamTransactions'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean())
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]))
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonAvgTransactions(osDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Win Percentage     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonWinPct(df):
    df = df[df.isActiveCoach ==1]
    pltTitle = 'Regular Season Win Percentage'
    pltXLabel = 'Percent of regular season matchups that are wins'
    pltFile = 'plots/reg_season_win_pct.png'
    measureLabel = 'teamWinPctRegSeason'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean()*100)
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*10)/10) + '%'
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonWinPct(osDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Avg Points For     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonAvgPointsFor(df):
    pltTitle = 'Regular Season Average Points'
    pltXLabel = 'Average points scored in regular season weekly matchups'
    pltFile = 'plots/reg_season_avg_points_for.png'
    measureLabel = 'teamWeekTotal'
    temp = df.groupby(['coach','isActiveCoach'])[measureLabel].mean()
    temp = temp.reset_index(level=['coach', 'isActiveCoach'])
    temp = temp[temp.isActiveCoach==1]
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.coach.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[temp.coach==label][measureLabel]))
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonAvgPointsFor(oswDf)
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Avg Points Against     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonAvgPointsAgainst(df):
    pltTitle = 'Regular Season Average Points Against'
    pltXLabel = 'Average points against in regular season weekly matchups'
    pltFile = 'plots/reg_season_avg_points_against.png'
    measureLabel = 'teamWeekTotalOpponent'
    temp = df.groupby(['coach','isActiveCoach'])[measureLabel].mean()
    temp = temp.reset_index(level=['coach', 'isActiveCoach'])
    temp = temp[temp.isActiveCoach==1]
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.coach.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[temp.coach==label][measureLabel]))
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonAvgPointsAgainst(oswDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Avg Weekly Rank     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonAvgWeeklyRank(df):
    pltTitle = 'Regular Season Average Weekly Rank'
    pltXLabel = 'Average weekly points rank in regular season matchups'
    pltFile = 'plots/reg_season_avg_weekly_rank.png'
    measureLabel = 'teamWeekRank'
    temp = df.groupby(['coach','isActiveCoach'])[measureLabel].mean()
    temp = temp.reset_index(level=['coach', 'isActiveCoach'])
    temp = temp[temp.isActiveCoach==1]
    temp = temp.sort_values(by=[measureLabel], ascending=False)
    labels = list(temp.coach.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[temp.coach==label][measureLabel]*10)/10)
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonAvgWeeklyRank(oswDf)


#~~~~~~~~~~~~~~~~~~~~~~~#
#     Highest Score     #
#~~~~~~~~~~~~~~~~~~~~~~~#
def plotMaxPoints(df):
    df = df[df.isActiveCoach ==1]
    measureLabel = 'teamWeekTotal'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].max())
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*10)/10)
        newLabels.append(newLabel)
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Highest Score')
    plt.xlabel('Most points ever scored')
    plt.savefig('plots/reg_season_max_points.png', dpi=200, bbox_inches='tight')

plotMaxPoints(oswDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Lowest Score     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonMinPoints(df):
    df = df[df.isActiveCoach ==1]
    df = df[df.isRegSeason == 1]
    measureLabel = 'teamWeekTotal'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].min())
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*10)/10)
        newLabels.append(newLabel)
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Regular Season Lowest Score')
    plt.xlabel('Fewest points ever scored during regular season')
    plt.savefig('plots/reg_season_min_points.png', dpi=200, bbox_inches='tight')

plotRegSeasonMinPoints(oswDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Ranking     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonRanking(df):
    df = df[df.isActiveCoach ==1]
    pltTitle = 'Regular Season Average Ranking'
    pltXLabel = 'Average ranking at the end of the regular season'
    pltFile = 'plots/reg_season_rank.png'
    measureLabel = 'teamRankRegSeason'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean())
    temp = temp.sort_values(by=[measureLabel], ascending=False)
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*10)/10)
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')
    
plotRegSeasonRanking(osDf)


#~~~~~~~~~~~~~~~~~~~~~~~#
#     Bullshit Wins     #
#~~~~~~~~~~~~~~~~~~~~~~~#    
def plotRegSeasonBullshitWins(df):
    pltTitle = 'Regular Season Bullshit Wins'
    pltXLabel = 'Percent of regular season wins that are bullshit'
    pltFile = 'plots/reg_season_bullshit_wins.png'
    measureLabel = 'bullshitWin'
    temp = df.groupby(['coach','isActiveCoach'])[measureLabel].mean()
    temp = temp.reset_index(level=['coach', 'isActiveCoach'])
    temp = temp[temp.isActiveCoach==1]
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.coach.values)
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[temp.coach==label][measureLabel]*10)/10) + '%'
        newLabels.append(newLabel)
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonBullshitWins(oswDf)


#~~~~~~~~~~~~~~~~~~~~~~~#
#     Shitty Losses     #
#~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonShittyLosses(df):
    pltTitle = 'Regular Season Shitty Losses'
    pltXLabel = 'Percent of regular season losses that are shitty'
    pltFile = 'plots/reg_season_shitty_losses.png'
    measureLabel = 'shittyLoss'
    temp = df.groupby(['coach','isActiveCoach'])[measureLabel].mean()
    temp = temp.reset_index(level=['coach', 'isActiveCoach'])
    temp = temp[temp.isActiveCoach==1]
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.coach.values)
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[temp.coach==label][measureLabel]*10)/10) + '%'
        newLabels.append(newLabel)
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonShittyLosses(oswDf)


#~~~~~~~~~~~~~~~~~~~~~~~#
#     Poor Coaching     #
#~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonPoorCoaching(df):
    df = df[df.isActiveCoach==1]
    pltTitle = 'Regular Season Poor Coaching Percentage'
    pltXLabel = 'Percent of regular season players played that got less than 0 points'
    pltFile = 'plots/reg_season_poor_coaching.png'
    measureLabel = 'poorCoaching'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean()*100)
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values)
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*10)/10) + '%'
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonPoorCoaching(oswpDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Bench Composition     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonBenchComposition(df):
    df = df[df.isActiveCoach==1]
    pltTitle = 'Regular Season Bench Composition'
    pltXLabel = 'Percentage breakdown of positions on your bench'
    pltFile = 'plots/reg_season_bench_composition.png'
    df = df[df.playerRosterPosition == 'BN']
    df = df[df.isRegSeason == 1]
    measureLabel = 'playerPosition'
    numerator = pd.DataFrame(df.groupby(['coach', measureLabel]).size(), columns=['numerator']).reset_index()
    denominator = pd.DataFrame(df.groupby(['coach']).size(), columns=['denominator'])
    df = pd.merge(numerator, denominator, on=['coach'])
    df['percent'] = df['numerator']/df['denominator']*100
    
    pivot_df = df.pivot(index='coach', columns=measureLabel, values='percent')
    pivot_df = pivot_df.fillna(0)
    pivot_df = pivot_df[['RB','WR','QB','TE','K','DEF','DP']]
    
    pivot_df.plot.bar(stacked=True)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')
    
plotRegSeasonBenchComposition(oswpDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Matchup Win Percentage     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonMatchupWinPercentage(df):
    pltTitle = 'Regular Season Matchup Win Percentage'
    pltFile = 'plots/reg_season_matchup_win_percent.png'
    measureLabel = 'isWin'
    df = df[df['isRegSeason'] == 1]
    df = df[df['isActiveCoach'] == 1]
    df = df[df['isActiveCoachOpponent'] == 1]
    temp = df.groupby(['coach', 'coachOpponent']).mean()*100
    temp = temp.round(0)
    temp = temp.reset_index(level=['coach', 'coachOpponent'])
    temp = temp.pivot(index='coach', columns='coachOpponent', values=measureLabel)
    plt.title(pltTitle)
    ax = sns.heatmap(temp, cmap="RdYlGn", annot=True, fmt='g')
    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonMatchupWinPercentage(oswDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Matchup Play Frequency     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonMatchupCompeteFrequency(df):
    pltTitle = 'Regular Season Matchup Compete Frequency'
    pltFile = 'plots/reg_season_matchup_compete_freq.png'
    measureLabel = 'isWin'
    df = df[df['isRegSeason'] == 1]
    df = df[df['isActiveCoach'] == 1]
    df = df[df['isActiveCoachOpponent'] == 1]
    temp = df.groupby(['coach', 'coachOpponent']).count()
    temp = temp.reset_index(level=['coach', 'coachOpponent'])
    temp = temp.pivot(index='coach', columns='coachOpponent', values=measureLabel)
    plt.title(pltTitle)
    ax = sns.heatmap(temp, cmap="RdYlGn", annot=True, fmt='g')
    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRegSeasonMatchupCompeteFrequency(oswDf)


#~~~~~~~~~~~~~~~~~~~~~~~~#
#     Rank By Season     #
#~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRankBySeason(df, start, end, grpNbr):
    df = df[df['isActiveCoach'] == 1]
    measureLabel = 'teamRankRegSeason'
    measureLabel = 'teamFinalStanding'
    df[measureLabel] = df[measureLabel]*-1
    pivDf = df.pivot(index='season', columns='coach', values=measureLabel)
    oldLabels = np.arange(-1,-13,-1)
    newLabels = np.arange(1,13,1)
    pltTitle = 'Rank By Season'
    pltFile = f'plots/rank_by_season{grpNbr}.png'
    subsetDf = pivDf[pivDf.columns[start:end]]
    plt.plot(subsetDf)
    plt.title(pltTitle)
    plt.yticks(ticks=oldLabels, labels=newLabels)
    plt.legend(subsetDf.columns)
    plt.xlabel('Season')
    plt.ylabel('Rank')
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotRankBySeason(osDf, 0, 3, 0)
plotRankBySeason(osDf, 3, 6, 1)
plotRankBySeason(osDf, 6, 9, 2)
plotRankBySeason(osDf, 9, 12, 3)


#~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Player Retention     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotPlayerRetention(df):
    df = df[df.isActiveCoach==1]
    df = df[['season', 'week', 'coach', 'playerNameAndInfo']]
    # Get max weeks for each season
    weeksDf = df[['season','week']]
    weeksDf = weeksDf.groupby(['season']).max()
    weeksDf = weeksDf.reset_index(level=['season'])
    # Join dataframes to see how much has changed
    startDf = df[df.week==1].rename(columns={"week": "weekStart"})
    endDf = pd.merge(df, weeksDf, how='inner', on=['season','week'])
    endDf = endDf.rename(columns={"week": "weekEnd"})
    changeDf = pd.merge(startDf, endDf, how='left', on=['season','coach','playerNameAndInfo'])
    changeDf = changeDf.fillna(0)
    def addSameIndicator(row):
        if row['weekEnd'] != 0:
            return 1
        else:
            return 0
    changeDf['playerRetained'] = changeDf.apply(addSameIndicator, axis=1)
    # Plot
    pltTitle = 'Player Retention Percentage'
    pltXLabel = 'Percentage of players that you kept the entire season'
    pltFile = 'plots/player_retention.png'
    measureLabel = 'playerRetained'
    temp = pd.DataFrame(changeDf.groupby('coach')[measureLabel].mean()*100)
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]*10)/10) + '%'
        newLabels.append(newLabel)
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

plotPlayerRetention(oswpDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Defensive Player Analyses     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def defensive_player_bar_std(df):
    def player_roster_position(row):
        '''
        Code flex players in roster postition
        '''
        rawPlayerPostition = row['playerRosterPosition']
        playerPosition = None
        flex_positions = ['R/W/T', 'W/R']
        if rawPlayerPostition in flex_positions:
            playerPosition = 'Flex'
        else:
            playerPosition = rawPlayerPostition
        return playerPosition
    
    # Filter data to population we care about
    df = df[df.isRegSeason==1] # Only want weeks where all coaches are trying
    df['playerRosterPosition'] = df.apply(player_roster_position, axis=1)
    df = df[df.playerPosition!='Empty']
    df = df[df.playerRosterPosition!='BN']
    df = df[df.playerRosterPosition!='RES']
    
    # Sum stats by roster position (sum RB and WR)
    df_sum = df.groupby(['coach', 'season', 'week', 'playerRosterPosition'])['playerPoints'].sum()
    df_sum = df_sum.reset_index()
    stats_df = df_sum.groupby('playerRosterPosition')['playerPoints'].describe()
    stats_df['68%'] = df_sum.groupby('playerRosterPosition')['playerPoints'].quantile(0.68)
    stats_df['95%'] = df_sum.groupby('playerRosterPosition')['playerPoints'].quantile(0.95)
    stats_df['97.7%'] = df_sum.groupby('playerRosterPosition')['playerPoints'].quantile(0.977)
    stats_df = stats_df.sort_values(by=['std'])
    
    # Plot elements
    pltTitle = 'Roster Position Average Total Points and Standard Deviations'
    pltXLabel = 'Average points scored by roster postion in regular season weekly matchups'
    pltFile = 'plots/dp_bar_std.png'
    labels = list(stats_df.index)
    y_pos = np.arange(len(stats_df))
    x_mean = stats_df['mean']
    x_68 = stats_df['68%']
    x_95 = stats_df['95%']
    x_97 = stats_df['97.7%']
    plt.barh(y_pos, x_mean)
    plt.legend(['mean'])
    plt.plot(x_68, y_pos, marker='D', linestyle='', color="b")
    plt.plot(x_95, y_pos, marker='D', linestyle='', color="orange")
    plt.plot(x_97, y_pos, marker='D', linestyle='', color="g")
    plt.yticks(y_pos, labels)
    plt.title(pltTitle)
    plt.xlabel(pltXLabel)
    plt.legend(['1 std (68th percentile)', '2 std (95th percentile)', '3 std (97.7th percentile)'])
    plt.savefig(pltFile, dpi=200, bbox_inches='tight')

defensive_player_bar_std(oswpDf)


