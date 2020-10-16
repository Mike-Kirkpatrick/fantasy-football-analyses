# Fantasy Football Analyses 2011-2019

### Brief Introduction
We've been playing fantasy football together for a while so it's time to examine our data longitudinally. Now, I know that words are hard, so I've used as few as possible. Charts, charts and more charts.

**Differences From Last Report:** I only included people that are currently active in the league. See the archived original report for statistics for innactive people.

I used python to web-scrape all of the data from our league's history. If you'd like to recreate these analyses for another NFL Fantasy Football league, you could recycle my code easily. 


## Coaches

### Seasons Participated
Every season we've had 12 coaches. You get a dot for each season you've participated.
![Alt text](./plots/seasons_participated.png?raw=true)


## Regular Season and Playoffs
Statistics for stuff that happens during the playoffs and the regular season.

### Max Points
Aaron has the highest score of all time. Fun fact is that he got this score during the championship game in our first season.
![Alt text](./plots/reg_season_max_points.png?raw=true)

### Min Points
Points are good, so having few points is bad. This plot is the lowest score you've ever scored. Hopefully your name is towards the top of this chart.
![Alt text](./plots/reg_season_min_points.png?raw=true)

### Trades
Yeah, we don't trade...ever. Most people have never traded. We should become more trusting of each other.
![Alt text](./plots/reg_season_trades.png?raw=true)

### Player Retention
Some of you are extremely loyal to your draft picks and some of you have an entirely new team by the end of the season. I compared which players you had during week one and which players you had in the championship week. If you had all the same players at the end of the season, you would have 100% player retention. On average, Danny keeps 59% of his players the entire season, whereas Alex keeps only 35%.
![Alt text](./plots/player_retention.png?raw=true)

### Transactions
Relatedly, we can look at the number of transactions. Alex basically has a new team every week. Given that there are 16 weeks in the regular season, Aaron and Danny change out less than one player per week.
![Alt text](./plots/reg_season_transactions.png?raw=true)


## Regular Season
Statistics for stuff that happens during the regular season.

### Win Percentage
This one is as straightforward as it gets. How often do you win? Hopefully you find your name at the top of this chart. Or, at the very least, have a winning record overall (i.e., > 50%).
![Alt text](./plots/reg_season_win_pct.png?raw=true)

### Matchup Rivalries
How often to you beat the other coaches during the regular season? Here's a heatmap of just that. Find your name on the left and see where it intersects with the people on the bottom. That is how often (%) you've beat that person. Green is good and red is bad. The second plot shows how many times you've played that person.

For example, I have beat Aaron only 14% of the time and we've played each other 14 times. Incredibly, Mike Thomas has beat Danny 100% of the time and they've played each other 9 times! Another thing we learn here is THE NEED TO ALWAYS SHUFFLE THE MATCHUP ORDER AJ!!! We've only had 9 seasons and AJ and Kameron have played each other 18 times during the regular season.
![Alt text](./plots/reg_season_matchup_win_percent.png?raw=true)
![Alt text](./plots/reg_season_matchup_compete_freq.png?raw=true)

### End of Season Rank
For these charts, you want to see low numbers next to your name. There's a pretty wide spread across all coaches. Mike Thomas consistently finishes well, but has never gotten 1st place. Always a bridesmaid and never a bride :)
![Alt text](./plots/reg_season_rank.png?raw=true)

### Average Points Against
These are the points that are scored against you. Looking at all seasons, it's pretty consistent for each coach.
![Alt text](./plots/reg_season_avg_points_against.png?raw=true)

### Average Points For
These are the points that you score each week. The distribution is a little more spread out than Points Against. Kameron proudly sits atop the list and Matt wallows in shame at the bottom.
![Alt text](./plots/reg_season_avg_points_for.png?raw=true)

### Average Weekly Rank
Each week, there are 12 teams that play in 6 matchups. Instead of looking at the results of the matchups, this is a ranking of all 12 teams from highest score (#1) to lowest score (#12) for the given week. I then took the average across all weeks/seasons. It's similar to Average Points For, except that this measure is robust to bye weeks. Hopefully you find your name towards the top of this list.
![Alt text](./plots/reg_season_avg_weekly_rank.png?raw=true)

### Bullshit Wins
Bullshit wins are an extension of weekly rank. A bullshit win occurs when someone wins their weekly matchup but their weekly score was ranked 7 or worse. That means that the person won despite having a lower score than half of the league. This is considered bullshit because, had you played almost anyone else that week, you would have lost. The percentage of bullshit wins is calculated by taking the number of wins that are bullshit divided by your total number of wins. Danny tops the chart with 40% of his wins being bullshit.
![Alt text](./plots/reg_season_bullshit_wins.png?raw=true)

### Shitty Losses
Shitty losses are the exact opposite of bullshit wins. A shitty loss occurs when you lose but had a weekly rank of 6 or better. For example, you got the 2nd highest points this week but you played the person who got the 1st highest points. Had you played anyone else, you would have won. It's a shitty loss. To calculate this, I took the number of losses divided by your total number of losses. Rob tops the chart with over a third of his losses being shitty.
![Alt text](./plots/reg_season_shitty_losses.png?raw=true)

### Poor Coaching
I wanted to get a measure of coaches giving up, being lazy and basically just not caring. Think of starting someone on IR, starting someone that's on bye or forgetting to roster a position entirely. Unfortunately, NFL FF doesn't save all of the player history, so I had to settle for analyzing how often you rostered a position that got 0 or fewer points. Our fabulous Commisioner tops the chart (shame!). On the other end of the spectrum, Alex and Rob do a consistently good job at setting their lineup.
![Alt text](./plots/reg_season_poor_coaching.png?raw=true)

### Bench Composition
I think there is a lot to unpack out of these last two plots, so I'll leave that to you.
![Alt text](./plots/reg_season_bench_composition.png?raw=true)


## Playoffs
Statistics for stuff that happens during the playoffs.

### Playoff Appearances
Mike Thomas has made it to the playoffs 6 out of 8 times which is very impressive.
![Alt text](./plots/playoff_appearances.png?raw=true)

### Playoff Medalists
Everyone that isn't named Alex or Matt has gotten 3rd or better at some point.
![Alt text](./plots/playoff_medalist.png?raw=true)

### Playoff Champions
Kameron has won thrice. AJ has won twice. Brian, Sam, Aaron and myself have won once.
![Alt text](./plots/playoff_champion.png?raw=true)

### Rank by Season
With the next four plots, we're looking at your rank (y-axis) at the end of each season (x-axis). For 11 of us, there's no real pattern. It's just a jumbled mess. One season you're good - the next you suck. However, for Kameron, there is a clear rise to power. He has improved his ranking every season since 2012, culminating with 3 successive championships. We hate you Kameron #AnyoneButBurt2020
![Alt text](./plots/rank_by_season0.png?raw=true)
![Alt text](./plots/rank_by_season1.png?raw=true)
![Alt text](./plots/rank_by_season2.png?raw=true)
![Alt text](./plots/rank_by_season3.png?raw=true)
