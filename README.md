# Fantasy Football Analyses 2011-2018

### Brief Introduction
We've been playing fantasy football together for a while so it's time to examine our data longitudinally. I used python to web-scrape all of the data from our league's history. If you'd like to recreate these analyses for another NFL Fantasy Football league, you could recycle my code easily. Now, I know that words are hard, so I've used as few as possible. Charts, charts and more charts. I consider this report as the first of many. I have a bunch of ideas to dig into our gameplay (or lack thereof) that I didn't have time to include this time around. If you have any ideas, let me know! 


## Coaches

### Seasons Participated
Every season we've had 12 coaches. You get a dot for each season you've participated.
![Alt text](./plots/seasons_participated.png?raw=true)


## Playoffs and Regular Season
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


### Transactions
Some of you are extremely loyal to your draft picks and some of you have an entirely new team by the end of the season. Alex basically has a new team every week. Given that there are 16 weeks in the regular season, Aaron changes out roughly one player per week.
![Alt text](./plots/reg_season_transactions.png?raw=true)

The last 5 seasons look very similar to all seasons. It appears that we have our own strategy and we stick to it.
![Alt text](./plots/reg_season_transactions_last5seasons.png?raw=true)


## Playoffs
Statistics for stuff that happens during the playoffs.

### Playoff Appearances
Alex and Nathan have made it to the playoffs 2 out of 2 times, which is impressive. However, Mike Thomas has made it to the playoffs 6 out of 7 times which is very impressive.
![Alt text](./plots/playoff_appearances.png?raw=true)

### Playoff Champions
AJ and Kameron have won twice. Brian, Sam, Aaron and myself have won once.
![Alt text](./plots/playoff_champion.png?raw=true)

### Playoff Medalists
Most people have gotten 3rd or better at some point.
![Alt text](./plots/playoff_medalist.png?raw=true)


## Regular Season
Statistics for stuff that happens during the regular season.


### Win Percentage
This one is as straightforward as it gets. How often do you win? Hopefully you find your name at the top of this chart. Or, at the very least, have a winning record overall (i.e., > 50%).
![Alt text](./plots/reg_season_win_pct.png?raw=true)

Looking at the last 5 seasons, there is a little shift in the order. A few people jumped up and a few dropped.
![Alt text](./plots/reg_season_win_pct_last5seasons.png?raw=true)


### End of Season Rank
For these charts, you want to see low numbers next to your name. There's a pretty wide spread across all coaches. 
![Alt text](./plots/reg_season_rank.png?raw=true)

Looking at the last 5 seasons, there's definitely a contraction at the top. There's a few people that consistently rank high at the end of the season and everyone else is 7 or higher. You can see some movement, but since there are so few data points being, one bad season can ruin your average.
![Alt text](./plots/reg_season_rank_last5seasons.png?raw=true)


### Average Points Against
These are the points that are scored against you. Looking at all seasons, it's pretty consistent for each coach.
![Alt text](./plots/reg_season_avg_points_against.png?raw=true)

However, looking at the last 5 seasons, it's rather suspicious that our commisioner is at the bottom of this list...
![Alt text](./plots/reg_season_avg_points_against_last5seasons.png?raw=true)


### Average Points For
These are the points that you score each week. The distribution is a little more spread out than Points Against. Kameron proudly sits atop the list.
![Alt text](./plots/reg_season_avg_points_for.png?raw=true)

Looking at the last 5 seasons, it appears that the wealth-gap has widened. The rich have gotten richer and the poor have gotten poorer.
![Alt text](./plots/reg_season_avg_points_for_last5seasons.png?raw=true)


### Average Weekly Rank
Each week, there are 12 teams that play in 6 matchups. Instead of looking at the results of the matchups, this is a ranking of all 12 teams from highest score (#1) to lowest score (#12) for the given week. I then took the average across all weeks/seasons. It's similar to Average Points For, except that this measure is robust to bye weeks. Hopefully you find your name towards the top of this list.
![Alt text](./plots/reg_season_avg_weekly_rank.png?raw=true)

Looking at the last 5 seasons, we see a similar trend: certain players are trending upwards while others are slowly sinking.
![Alt text](./plots/reg_season_avg_weekly_rank_last5seasons.png?raw=true)


### Bullshit Wins
Bullshit wins are an extension of weekly rank. A bullshit win occurs when someone wins their weekly matchup but their weekly score was rank 7 or worse. That means that the person won despite have a lower score than half of the league. This is considered bullshit because, had you played almost anyone else that week, you would have lost. The percentage of bullshit wins is calculated by taking the number of wins that are bullshit divided by your total number of wins. Danny tops the chart with 40% of his wins being bullshit.
![Alt text](./plots/reg_season_bullshit_wins.png?raw=true)

Looking at the last 5 seasons, the bullshit is getting more and more polarized. Half of the time that Danny wins, it's bullshit.
![Alt text](./plots/reg_season_bullshit_wins_last5seasons.png?raw=true)


### Shitty Losses
Shitty losses are the exact opposite of bullshit wins. A shitty loss occurs when you lose but had a weekly rank of 6 or better. For example, you got the 3rd highest points this week but you played the person who got the 2nd highest points. Had you played almost anyone else, you would have won. It's a shitty loss. To calculate this, I took the number of losses divided by your total number of losses. Rob tops the chart with over a third of his losses being shitty.
![Alt text](./plots/reg_season_shitty_losses.png?raw=true)

Looking at the last 5 seasons, AJ leaps ahead while others drop lower.
![Alt text](./plots/reg_season_shitty_losses_last5seasons.png?raw=true)


### Poor Coaching
I wanted to get a measure of coaches giving up, being lazy and basically just not caring. Think of starting someone on IR, starting someone that's on bye or forgetting to roster a position entirely. Unfortunately, NFL FF doesn't save all of the player history. So, I had to settle for analyzing how often you rostered a position that got 0 or fewer points. Matt Smith tops the charts across all seasons and for the last 5 seasons. Matt Cicneros is also consistenly high. On the other end of the spectrum, Alex and Rob do a consistently good job at setting their lineup.
![Alt text](./plots/reg_season_poor_coaching.png?raw=true)

![Alt text](./plots/reg_season_poor_coaching_last5seasons.png?raw=true)


### Bench Composition
I think there is a lot to unpack out of these last two plots, so I'll leave that to you.
![Alt text](./plots/reg_season_bench_composition.png?raw=true)

![Alt text](./plots/reg_season_bench_composition_last5seasons.png?raw=true)
