# Fantasy Football Analyses 2011-2023

### Brief Introduction
We've been playing fantasy football together for a while so it's time to examine our data longitudinally. Now, I know that words are hard, so I've used as few as possible. Charts, charts and more charts.

**Note:** I only included people that are active in the most recent season. See the first archived report for statistics for innactive people.

I used python to web-scrape all of the data from our league's history. If you'd like to recreate these analyses for another NFL Fantasy Football league, you could recycle my code easily. 


## Coaches

### Seasons Participated
Every season we've had 12 coaches. You get a dot for each season you've participated.
![Alt text](./plots/seasons_participated.png?raw=true)

## Defensive Player Roster Position
### Individual Defensive Player Is Stupid and You Are Too If You Like It
The people have spoken and IDP is gone! Woohoo! I'm including this section this year just one more time for fun and as reinforcement of the uselessness of IDP given that the results are unchanged.

This year I'm including a special section dedicated to the individual defensive player (DP) roster position. To examine the relevance of the DP position on our roster, I filtered the data to the regular season and included only players that were actually started for the week (no bench). This is important - we're only looking at the players that were actually started (arguably the top 12 players for that position for the week (top 24 for RB and WR)). For the given coach-season-week, I combined the points for the two running back roster spots together, and also did the same for wide receivers. I did this because I wanted to assess the value of each roster position. In line with this, I categorized the flex roster position as "flex" instead of bucketing those players into either RB, WR, or TE. I then calculated the mean and standard deviation/percentiles for each roster position across all our seasons. The results are in the plot below.

As you can see in the chart, running backs, wide receivers and quarterbacks are by far the most important. Your two running backs combined will score, on average, around 23 points. On a slightly above average week (1 standard deviation/68th percentile), you'll get around 28 points. On a super good week (3 standard deviations/97.7th percentile), you'll ball out and get nearly 50 points. There is a huge amount of variability for these roster spots, which makes seeking out the best players for these positions of the utmost importance.

Looking at the other positions (Flex, Def, TE, K, DP), they all have similar means. But what matters is how wide their standard deviations are. This relates to the variance you expect for that roster position. With the Flex, Def and TE spot, there's a ton of variability. The variability is what makes the roster position worthwhile. You want to get the good players for that position because they can significantly outscore your opponent (this is the reason why Travis Kelce is always drafted early). Looking at the DP position, on average you'll get around 8 points. On the most amazing week (97.7th percentile), you'll get around 15 points. What's the point (pun intended) of this? It doesn't matter which of the top 12 DP's you choose for a given week. They all do more or less the same. Now, I know what you're thinking... "Mike, what about the kicker? They're pretty similar to DP." You are correct! I think it's fine to have one useless, non-strategic position on our roster. But two is too many. Just like there's only room for one AJ in our group ;)
![Alt text](./plots/dp_bar_std.png?raw=true)

## Regular Season and Playoffs
Statistics for stuff that happens during the playoffs and the regular season.

### Max Points
Aaron has the highest score of all time. Fun fact is that he got this score during the championship game in our first season. But Aaron is a quiter so we don't care about him anymore. Rob has the highest points ever now (as of the most recent season, too). Congrats, Rob.
![Alt text](./plots/reg_season_max_points.png?raw=true)

### Min Points
Points are good, so having few points is bad. This plot is the lowest score you've ever scored. Hopefully your name is towards the top of this chart.
![Alt text](./plots/reg_season_min_points.png?raw=true)

### Trades
Yeah, we don't trade...ever. Most people have never traded. We should become more trusting of each other.
![Alt text](./plots/reg_season_trades.png?raw=true)

### Player Retention
Some of you are extremely loyal to your draft picks and some of you have an entirely new team by the end of the season. I compared which players you had during week one and which players you had in the championship week. If you had all the same players at the end of the season, you would have 100% player retention. On average, Matt Smith keeps 62% of his players the entire season, whereas Alex keeps only 38%.
![Alt text](./plots/player_retention.png?raw=true)

### Transactions
Relatedly, we can look at the number of transactions. Alex basically has a new team every week. Given that there are 16-17 weeks in the regular season, AJ, Colin and Danny change out less than one player per week (there are only so many Bills players that Colin can pick up each week).
![Alt text](./plots/reg_season_transactions.png?raw=true)


## Regular Season Only
Statistics for stuff that happens during the regular season.

### Win Percentage
This one is as straightforward as it gets. How often do you win? Hopefully you find your name at the top of this chart. Or, at the very least, have a winning record overall (i.e., > 50%).
![Alt text](./plots/reg_season_win_pct.png?raw=true)

### Matchup Rivalries
How often do you beat the other coaches during the regular season? Here's a heatmap of just that. Find your name on the left and see where it intersects with the people on the bottom. That is how often (%) you've beat that person. Green is good and red is bad. The second plot shows how many times you've played that person.

For example, Sam has beat Kameron only 15% of the time and they've played each other 13 times. Unfortunately, Danny has broken the losing streak to Mike Thomas. Cheers, Dan. But on a good note, Alex is emerging as undefeated against Matt Smith and they're played each other 4 time sso far. Another thing we learn here is THE NEED TO ALWAYS SHUFFLE THE MATCHUP ORDER, AJ! We've had had 13 seasons and AJ has played Kameron 23 times during the regular season.
![Alt text](./plots/reg_season_matchup_win_percent.png?raw=true)
![Alt text](./plots/reg_season_matchup_compete_freq.png?raw=true)

### End of Season Rank
For these charts, you want to see low numbers next to your name. There's a pretty wide spread across all coaches. Mike Thomas consistently finishes well, but has never gotten 1st place.
![Alt text](./plots/reg_season_rank.png?raw=true)

### Average Points Against
These are the points that are scored against you. Looking at all seasons, it's pretty consistent for each coach.
![Alt text](./plots/reg_season_avg_points_against.png?raw=true)

### Average Points For
These are the points that you score each week. The distribution is a little more spread out than Points Against. Kameron proudly sits atop the list while Matt Cisneros wallows in shame at the bottom.
![Alt text](./plots/reg_season_avg_points_for.png?raw=true)

### Average Weekly Rank
Each week, there are 12 teams that play in 6 matchups. Instead of looking at the results of the matchups, this is a ranking of all 12 teams from highest score (#1) to lowest score (#12) for the given week. I then took the average across all weeks/seasons. It's similar to Average Points For, except that this measure is robust to bye weeks. Hopefully you find your name towards the top of this list.
![Alt text](./plots/reg_season_avg_weekly_rank.png?raw=true)

### Bullshit Wins
Bullshit wins are an extension of weekly rank. A bullshit win occurs when someone wins their weekly matchup but their weekly score was ranked 7 or worse. That means that the person won despite having a lower score than half of the league. This is considered bullshit because, had you played almost anyone else that week, you would have lost. The percentage of bullshit wins is calculated by taking the number of wins that are bullshit divided by your total number of wins. Danny tops the chart with 37% of his wins being bullshit.
![Alt text](./plots/reg_season_bullshit_wins.png?raw=true)

### Shitty Losses
Shitty losses are the exact opposite of bullshit wins. A shitty loss occurs when you lose but had a weekly rank of 6 or better. For example, you got the 2nd highest points this week but you played the person who got the 1st highest points. Had you played anyone else, you would have won. It's a shitty loss. To calculate this, I took the number of losses divided by your total number of losses. Kam tops the chart with 39% of his losses being shitty.
![Alt text](./plots/reg_season_shitty_losses.png?raw=true)

### Bullshit Wins by Shitty Losses
This is a scatterplot of Bullshit Wins and Shitty Losses. If you find yourself in the top left, that means when you win, it is well earned. And when you lose, it's bad luck. If you find yourself in the bottom right, that means when you win, it's bullshit. And when you lose, it's well earned.
![Alt text](./plots/reg_season_bullshit_wins_by_shitty_losses.png?raw=true)

### Poor Coaching
I wanted to get a measure of coaches giving up, being lazy and basically just not caring. Think of starting someone on IR, starting someone that's on bye or forgetting to roster a position entirely. Unfortunately, NFL FF doesn't save all of the player history, so I had to settle for analyzing how often you rostered a position that got 0 or fewer points. On average, Matt Smith is the worst coach whereas Alex is the best.
![Alt text](./plots/reg_season_poor_coaching.png?raw=true)

### Bench Composition
I think there is a lot to unpack out of this last plot, so I'll leave that to you.
![Alt text](./plots/reg_season_bench_composition.png?raw=true)


## Playoffs Only
Statistics for stuff that happens during the playoffs.

### Playoff Appearances
Mike Thomas has made it to the playoffs 9 out of 12 times which is very impressive. Equally impressive is that, despite always making it to the playoffs, Mike has yet to bring home the trophy. Always a bridesmaid and never a bride :)
![Alt text](./plots/playoff_appearances.png?raw=true)

### Playoff Medalists
Everyone except Matt Cisneros has gotten 3rd or better at some point.
![Alt text](./plots/playoff_medalist.png?raw=true)

### Playoff Champions
Kameron has won Quarce. AJ and Rob has won twice (Rob being back to back for 2022 and 2023). Brian, Matt, Sam, and myself.
![Alt text](./plots/playoff_champion.png?raw=true)

### Rank by Season
With the next four plots, we're looking at your rank at the end of each season. For 11 of us, there's no real pattern. It's just a jumbled mess. One season you're good - the next you suck. However, for Kameron, there is a clear rise to power starting in 2012 and culminating with 4 successive championships from 2017 to 2020. We hate you, Kameron, and it has been wonderful watching you lose the last 3 years. Let's keep that going. #AnyoneButBurt. Also, Rob, we're beginning to hate you too. Two wins in a row is too many. #AnyoneButBurtButAlsoMaybeNotManbertToo
![Alt text](./plots/rank_by_season0.png?raw=true)
![Alt text](./plots/rank_by_season1.png?raw=true)
![Alt text](./plots/rank_by_season2.png?raw=true)
![Alt text](./plots/rank_by_season3.png?raw=true)
