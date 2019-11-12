#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 22:30:03 2019

@author: mike
"""

Ideas:
    Regular season:
        -Win percentage
        -Average rank
        Average points for
        Average points against
        -Bullshit wins
        -Shitty losses
        highest score ever
        Lowest score ever
        Bench composition
        -Poor Coaching (players with 0 points not on bench)
        Transactions
    Playoffs:
        Most appearances
        Most wins
    General Trends:
        Average points per week
    See if players that win during the week actually influence the fantasy outcome


from os import chdir
chdir('/home/mike/fantasy-football-analyses')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

osDf = pd.read_csv('data_owner_season.csv')
oswDf = pd.read_csv('data_owner_season_week.csv')
oswpDf = pd.read_csv('data_owner_season_week_player.csv')

def assignCoach(row):
    '''Aj has a space after is name like an ass'''
    teamOwner = row['teamOwner']
    teamName = row['teamName']
    coach = ''
    if teamOwner == 'AJ ':
        coach = 'Aj Crane'
    if teamOwner == 'AJ':
        coach = 'Aj Crane'
    if teamOwner == 'Aaron':
        coach = 'Aaron Horwitz'
    if teamOwner == 'Alex':
        coach = 'Alex Price'
    if teamOwner == 'Brian':
        coach = 'Brian Hazzel'
    if teamOwner == 'Colin':
        coach = 'Colin Rehbein'
    if teamOwner == 'Jason':
        coach = 'Jason Murphy'
    if teamOwner == 'Kameron':
        coach = 'Kameron Burt'
    if teamOwner == 'Matt':
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
    if teamOwner == 'dan':
        coach = 'Dan Tarin'
    if teamOwner == 'nathan':
        coach = 'Nathan Radolf'
    return coach

osDf['coach'] = osDf.apply(assignCoach, axis=1)
oswDf['coach'] = oswDf.apply(assignCoach, axis=1)
oswpDf['coach'] = oswpDf.apply(assignCoach, axis=1)


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





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Win Percentage     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonWinPct(df):
    measureLabel = 'teamWinPctRegSeason'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean()*100)
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label])) + '%'
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Regular Season Win Percentage')
    plt.xlabel('Percent of regular season matchups that are wins')
    plt.savefig('plots/reg_season_win_pct.png', dpi=200, bbox_inches='tight')
    

plotRegSeasonWinPct(osDf)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Regular Season Ranking     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotRegSeasonRanking(df):
    measureLabel = 'teamRankRegSeason'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean())
    temp = temp.sort_values(by=[measureLabel], ascending=False)
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label]))
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Regular Season Average Ranking')
    plt.xlabel('Average ranking at the end of the regular season')
    plt.savefig('plots/reg_season_rank.png', dpi=200, bbox_inches='tight')
    
plotRegSeasonRanking(osDf) 


#~~~~~~~~~~~~~~~~~~~~~~~#
#     Bullshit Wins     #
#~~~~~~~~~~~~~~~~~~~~~~~#
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


def plotBullshitWins(df):
    temp = pd.DataFrame(df.groupby('coach')['bullshitWin'].mean())
    temp = temp.sort_values(by=['bullshitWin'])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp['bullshitWin'][label])) + '%'
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp['bullshitWin'])
    plt.yticks(y_pos, newLabels)
    plt.title('Bullshit Wins')
    plt.xlabel('Percent of regular season wins that are bullshit')
    plt.savefig('plots/bullshit_wins.png', dpi=200, bbox_inches='tight')

plotBullshitWins(oswDf)




#~~~~~~~~~~~~~~~~~~~~~~~#
#     Shitty Losses     #
#~~~~~~~~~~~~~~~~~~~~~~~#
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

def plotShittyLosses(df):
    temp = pd.DataFrame(df.groupby('coach')['shittyLoss'].mean())
    temp = temp.sort_values(by=['shittyLoss'])
    labels = list(temp.index.values) 
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp['shittyLoss'][label])) + '%'
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp['shittyLoss'])
    plt.yticks(y_pos, newLabels)
    plt.title('Shitty Losses')
    plt.xlabel('Percent of regular season losses that are shitty')
    plt.savefig('plots/shitty_losses.png', dpi=200, bbox_inches='tight')

plotShittyLosses(oswDf)






#~~~~~~~~~~~~~~~~~~~~~~~#
#     Poor Coaching     #
#~~~~~~~~~~~~~~~~~~~~~~~#
def poorCoaching(row):
    poorCoaching = None
    if row['playerPosition'] != 'BN' and row['isRegSeason'] == 1:
        if row['playerPoints'] <= 0.0:
            poorCoaching = 1
        elif row['playerPoints'] > 0.0:
            poorCoaching = 0
    return poorCoaching

oswpDf['poorCoaching'] = oswpDf.apply(poorCoaching, axis=1)

def plotPoorCoaching(df):
    measureLabel = 'poorCoaching'
    temp = pd.DataFrame(df.groupby('coach')[measureLabel].mean()*100)
    temp = temp.sort_values(by=[measureLabel])
    labels = list(temp.index.values)
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label])) + '%'
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Regular Season Poor Coaching Percentage')
    plt.xlabel('Percent of regular season players played that got less than 0 points')
    plt.savefig('plots/reg_season_poor_coaching.png', dpi=200, bbox_inches='tight')

plotPoorCoaching(oswpDf)






#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     Bench Composition     #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def plotBenchComposition(df):
    df = df[df.playerRosterPosition == 'BN']
    measureLabel = 'playerPosition'
    numerator = pd.DataFrame(df.groupby(['coach', measureLabel]).size(), columns=['numerator']).reset_index()
    denominator = pd.DataFrame(df.groupby(['coach']).size(), columns=['denominator'])
    df = pd.merge(numerator, denominator, on=['coach'])
    df['percent'] = df['numerator']/df['denominator']*100
    
    pivot_df = df.pivot(index='coach', columns=measureLabel, values='percent')
    pivot_df = pivot_df.fillna(0)
    pivot_df = pivot_df[['QB','RB','WR','TE','K','DEF','DP']]
    
    pivot_df.plot.bar(stacked=True)
    
    
    
    
    
    labels = list(temp.index.values)
    y_pos = np.arange(len(temp))
    newLabels = []
    for label in labels:
        newLabel = label +' '+ str(int(temp[measureLabel][label])) + '%'
        newLabels.append(newLabel)
        
    plt.barh(y_pos, temp[measureLabel])
    plt.yticks(y_pos, newLabels)
    plt.title('Regular Season Poor Coaching Percentage')
    plt.xlabel('Percent of regular season players played that got less than 0 points')
    plt.savefig('plots/reg_season_poor_coaching.png', dpi=200, bbox_inches='tight')

plotPoorCoaching(oswpDf)



df = oswpDf


