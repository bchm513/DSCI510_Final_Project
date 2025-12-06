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

# Analysis

The multi-model approach—combining Random Forest and LassoCV—allowed for a more comprehensive evaluation of feature importance by capturing both the non-linear relationships (Random Forest) and the sparse, interpretable patterns (LassoCV) in the data. This comparative methodology provides a more holistic understanding of which statistics truly drive transfer success across different positions.

For each of the models, I focused on which features (football stats) predicted the metric of wick score, a holistic "all in one" type of statistic that measures the overall success of a player. In this analysis I was able to hone in on a few significant factors for each position. The variation in predictive factors between positions (single metric for Edge Defenders vs. multiple metrics for Linebackers) suggests that transfer evaluation strategies should be position-specific rather than applying a one-size-fits-all approach.

These findings can be leveraged to develop targeted recruitment strategies during the transfer window, enabling teams to identify high-potential transfer candidates based on quantifiable performance metrics aligned with each position's success profile.

# Results

Out of over a dozen different positions in college football, the analysis identified four positions with the highest transfer success rates: wide receivers, linebackers, edge defenders, and defensive backs. 

For Edge Defenders, a single key performance indicator emerged as the primary predictor of transfer success: pass rush ability. In contrast, Linebackers showed a more complex profile, with multiple statistics correlating with successful transfers, including pass rush, run defense, run defense snaps, and discipline metrics.

Both Random Forest and LassoCV models were employed to evaluate the statistical impact across positions, with each model highlighting different aspects of player performance and providing complementary insights into which metrics best predict transfer success. The Random Forest model was especially valuable in that it was able to detail exact thresholds of stats we should be targetting within the indicated position groups.

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