# Transfer Player Success <Project title>
In Pro Football Focus I have access to data about transfer players, and I want to gauge what college football players or types of players are most successful after transfering. I will isolate my findings by position, type of transfer, unit on the field, and success metrics I discuss later.

I plan on using various regression and decision tree models to capture the most significant variables that define player success after having filtered and cleaned the content to my liking.
_

# Data sources
| Index | Name             | URL       | Type | List of fields | Format | Collected?   | Estimated Data Size               |
|-------|-----------------|-----------|------|----------------|--------|-------------|---------------------------------|
| 1     | Player stats 2020 | See below | API  | See below      | JSON   | Yes, python | Tens of thousands of json entries |
| 2     | Player stats 2021 |           | API  |                | JSON   | Yes, python | Same as above                   |
| 3     | Player stats 2022 |           | API  |                | JSON   | Yes, python | Same as above                   |
| 4     | Player stats 2023 |           | API  |                | JSON   | Yes, python | Same as above                   |
| 5     | Player stats 2024 |           | API  |                | JSON   | Yes, python | Same as above                   |


# Results 
TBD

# Installation
pff api in .env file
duckdb
pandas


# Running analysis 
I am currently working to clean up the data and find specific positions that have enough data to make generalizations about. I will then deploy my models of choice and create visuals to depict the features most tied to player success

# Difficulties/Issues
No real issues or difficulties, but I have changed the scope of my project. I have expanded it because only focusing on the discipline stat seemed too limiting when I was considering how to develop my models.

From `src/` directory run:

`python main`

Results will appear in `results/` folder. All obtained will be stored in `data/`