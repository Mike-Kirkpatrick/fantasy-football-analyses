#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 22:30:03 2019

@author: mike
"""

Ideas:
    Regular season:
        Bullshit wins
        Shitty losses
        highest score ever
        Lowest score ever
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
        if teamOwner == 'Mr Pig Skinner':
            coach = 'Mike Thomas'
        elif teamOwner == 'MrPigSkinner':
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



#~~~~~~~~~~~~~~~~~~~~~~~#
#     Bullshit Wins     #
#~~~~~~~~~~~~~~~~~~~~~~~#
''' For each coach, what percent of your wins are bullshit wins?
    A bullshit win is when you win and your points is less than 
    the median points for the week'''
def bullshitWins(row):
    matchupResult = row['teamMatchupResult']
    weekRank = row['teamWeekRank']
    if matchupResult == 'Win' and weekRank >= 7:
        bsWin = 100
    else:
        bsWin = 0
    return bsWin

oswDf['bullshitWin'] = oswDf.apply(bullshitWins, axis=1)
temp = oswDf[oswDf['teamMatchupResult']=='Win']
temp = pd.DataFrame(temp.groupby('coach')['bullshitWin'].mean())
temp = temp.sort_values(by=['bullshitWin'])


labels = list(temp.index.values) 
y_pos = np.arange(len(temp))
plt.barh(y_pos, temp['bullshitWin'])
plt.yticks(y_pos, labels)
plt.title('Bullshit Wins')
plt.xlabel('Percent of wins that are bullshit')
plt.savefig('plots/bullshit_wins.png', bbox_inches='tight')
#plt.show()






















