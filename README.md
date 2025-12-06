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
| 6     | Wick Scores Data |           | drive  |                | CSV   | Yes, python | 20000+ csv rows                   |
| 7     | Snap Count Data |           | drive  |                | CSV   | Yes, python | 15000+ csv rows                   |


# Results 
Out of over a dozen different positions in college football, the clear most successful positions when it comes to transfering are wide receivers, linebackers, edge defenders and defensive backs. For positions like Edge Defenders, there is a clear stat that we can target to find the best transfers, that being "pass_rush". For the position of Linebacker, there are quite a few stats that we can look at that correlate with success, including "pass_rush", "run_defense", "run_defense_snaps", and discipline among many more. Using both Random Forest and LassoCV models to gauge the impact of various stats, I am able to cover more ground and compare and contrast the results of the models to get a more holistic sense of which stats are the most important. Ultimately, I can use this information to hone in on the best players to target in the transfer window in college football in order to improve the team in future years. 

# Installation

Install the required packages:
```bash
pip install pandas duckdb scikit-learn matplotlib requests aiohttp tenacity python-dotenv
```
If using a requirements.txt file:
```txt
pandas
duckdb
scikit-learn
matplotlib
requests
aiohttp
tenacity
python-dotenv
```

Then install with:
```bash
pip install -r requirements.txt
```

# How to Run

From `src/` directory run:

`python main`

or go through results.ipynb notebook and run each function manually. Results (model charts) will be generated from the content in analysis.py, but they have been replicated in the results/visuals folder for easy viewing. Keep in mind that join_ids_with_api takes a while to run. (I have commented out the actual running of that section and have just pulled the data from my google drive after copying it there). You need a PFF API key for this project, which you need to make an account for. That is the only required API key found in .env.