# ⚽ Football-Data Documentation

> Data is provided in **CSV format**, compatible with standard spreadsheet applications.
> Some older abbreviations may refer to bookmakers no longer in use — see [football-data.co.uk/matches.php](http://www.football-data.co.uk/matches.php) for the current list.

---

## 📋 Match Results

| Column | Description |
|--------|-------------|
| `Div` | League Division |
| `Date` | Match Date (dd/mm/yy) |
| `Time` | Kick-off time |
| `HomeTeam` | Home Team |
| `AwayTeam` | Away Team |
| `FTHG` / `HG` | Full Time Home Team Goals |
| `FTAG` / `AG` | Full Time Away Team Goals |
| `FTR` / `Res` | Full Time Result — `H` = Home Win, `D` = Draw, `A` = Away Win |
| `HTHG` | Half Time Home Team Goals |
| `HTAG` | Half Time Away Team Goals |
| `HTR` | Half Time Result — `H` = Home Win, `D` = Draw, `A` = Away Win |

---

## 📊 Match Statistics

> Not all statistics are available for every match/season.

| Column | Description |
|--------|-------------|
| `Attendance` | Crowd Attendance |
| `Referee` | Match Referee |
| `HS` / `AS` | Home / Away Team Shots |
| `HST` / `AST` | Home / Away Team Shots on Target |
| `HHW` / `AHW` | Home / Away Team Hit Woodwork |
| `HC` / `AC` | Home / Away Team Corners |
| `HF` / `AF` | Home / Away Team Fouls Committed |
| `HFKC` / `AFKC` | Home / Away Team Free Kicks Conceded |
| `HO` / `AO` | Home / Away Team Offsides |
| `HY` / `AY` | Home / Away Team Yellow Cards |
| `HR` / `AR` | Home / Away Team Red Cards |
| `HBP` / `ABP` | Home / Away Bookings Points (Yellow = 10pts, Red = 25pts) |

> **Note:** Free Kicks Conceded includes fouls, offsides, and other offences — always ≥ fouls.
> Used instead of fouls for France 2nd, Belgium 1st, and Greece 1st divisions.

> **Note:** English & Scottish yellow cards exclude the initial yellow when converted to a red,
> but European data includes it.

---

## 🎰 Betting Odds

Odds shown are **pre-closing**. For closing odds, append `C` to the abbreviation (e.g. `B365CH` = closing Bet365 home win odds).

### Match Result Odds (1X2)

| Column(s) | Bookmaker |
|-----------|-----------|
| `1XBH` / `1XBD` / `1XBA` | 1XBet |
| `B365H` / `B365D` / `B365A` | Bet365 |
| `BFH` / `BFD` / `BFA` | Betfair |
| `BFDH` / `BFDD` / `BFDA` | Betfred |
| `BMGMH` / `BMGMD` / `BMGMA` | BetMGM |
| `BVH` / `BVD` / `BVA` | Betvictor |
| `BWH` / `BWD` / `BWA` | Bet&Win |
| `CLH` / `CLD` / `CLA` | Coral |
| `GBH` / `GBD` / `GBA` | Gamebookers |
| `IWH` / `IWD` / `IWA` | Interwetten |
| `LBH` / `LBD` / `LBA` | Ladbrokes |
| `PSH` / `PH` / `PSD` / `PD` / `PSA` / `PA` | Pinnacle |
| `WHH` / `WHD` / `WHA` | William Hill |
| `MaxH` / `MaxD` / `MaxA` | Market Maximum Odds |
| `AvgH` / `AvgD` / `AvgA` | Market Average Odds |
| `BFEH` / `BFED` / `BFEA` | Betfair Exchange |

### BetBrain Aggregates

| Column | Description |
|--------|-------------|
| `Bb1X2` | Number of bookmakers used for averages/maximums |
| `BbMxH` / `BbAvH` | Max / Average home win odds |
| `BbMxD` / `BbAvD` | Max / Average draw odds |
| `BbMxA` / `BbAvA` | Max / Average away win odds |

---

## 🔢 Over/Under Goals Odds (2.5)

| Column | Description |
|--------|-------------|
| `BbOU` | Number of BetBrain bookmakers used |
| `BbMx>2.5` / `BbAv>2.5` | Max / Average over 2.5 goals |
| `BbMx<2.5` / `BbAv<2.5` | Max / Average under 2.5 goals |
| `GB>2.5` / `GB<2.5` | Gamebookers over / under 2.5 |
| `B365>2.5` / `B365<2.5` | Bet365 over / under 2.5 |
| `P>2.5` / `P<2.5` | Pinnacle over / under 2.5 |
| `Max>2.5` / `Max<2.5` | Market maximum over / under 2.5 |
| `Avg>2.5` / `Avg<2.5` | Market average over / under 2.5 |

---

## 🏷️ Asian Handicap Odds

| Column | Description |
|--------|-------------|
| `BbAH` | Number of BetBrain bookmakers used |
| `BbAHh` / `AHh` | Handicap size (home team) |
| `BbMxAHH` / `BbAvAHH` | Max / Average Asian handicap home odds |
| `BbMxAHA` / `BbAvAHA` | Max / Average Asian handicap away odds |
| `GBAHH` / `GBAHA` / `GBAH` | Gamebookers AH home / away / handicap |
| `LBAHH` / `LBAHA` / `LBAH` | Ladbrokes AH home / away / handicap |
| `B365AHH` / `B365AHA` / `B365AH` | Bet365 AH home / away / handicap |
| `PAHH` / `PAHA` | Pinnacle AH home / away |
| `MaxAHH` / `MaxAHA` | Market maximum AH home / away |
| `AvgAHH` / `AvgAHA` | Market average AH home / away |

---

## 🗂️ Data Sources

| Data Type | Source |
|-----------|--------|
| Results (FT, HT) | [XScores](http://www.xscores.com) |
| Match statistics | BBC, Flashscore, ESPN Soccer, Bundesliga.de, Gazzetta.it, Football.fr |
| Betting odds | [Betbrain.com](http://www.betbrain.com), [Oddsportal.com](http://www.oddsportal.com), Individual bookmakers |

> Odds for **weekend games** are collected on **Friday afternoons**.
> Odds for **midweek games** are collected on **Tuesday afternoons**.
