from processing import *
from data_retrieval import *
from analysis import *
import pandas as pd
import asyncio

import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


######### PROCESSING #########
# this section is for initial analysis and investigation, this does not use the actual data I will be using to create my models

# get wicks scores data for the transfers
transfer_player_snap_counts = retrieve_wicks()
# transfer_player_snap_counts

# get players who moved up in division
succeeded_df = make_moved_up_df(transfer_player_snap_counts)
# succeeded_moved_up_df

# filtered for successful players when they've moved
filtered = filter_for_successful()
# filtered

# get the rest of the stats tied to the successful players
succeeded_expanded_df = pd.read_csv("intermediate_content/succeeded_expanded.csv")
final_position_selection(succeeded_expanded_df)



######### DATA RETRIEVAL #########
# this section is for using the API to get the data and then filtering for the correct players from there

asyncio.run(get_api_main())

succeeded_ids_df = pd.read_csv("intermediate_content/succeeded_ids.csv")

# join_ids_with_api(succeeded_ids_df)



######### ANALYSIS #########
# this section is where my investigation into individual positions begins and I create my models/results

# get columns
column_list = get_columns()
# print(column_list)

# broad analysis for all positions
total_analysis()

# analysis for defensive backs
db_analysis()

# analysis for edge defenders
ed_analysis()

# analysis for linebackers
lb_analysis()

# analysis for wide receviers
wr_analysis()