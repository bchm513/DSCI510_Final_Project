##### This is the file where I go through the wick score data to filter out for the ids I need given the success of transfer players

def retrieve_wicks(snap_gid, snap_sheet_id, wick_gid, wick_sheet_id):
    import pandas as pd
    import requests
    import os

    ##### This is the data not gotten by the API, 
    ##### I will use this to get a sense of what to look for once I get API data

    ##### This was my old version of collecting the data straight from intermediate content
    # team_defense_snaps = pd.read_csv('intermediate_content/team_defense_snaps.csv')  
    # team_offense_snaps = pd.read_csv('intermediate_content/team_offense_snaps.csv')
    # transfer_player_career_wicks = pd.read_csv('intermediate_content/transfer_player_career_wicks.csv')
    # transfer_player_snap_counts = pd.read_csv('intermediate_content/transfer_player_snap_counts.csv')
    # transfer_player_career_wicks

    # get the wicks data information from google drive and send it directly to intermediate content folder
    csv_url = f"https://docs.google.com/spreadsheets/d/{wick_sheet_id}/export?format=csv&gid={wick_gid}"
    response = requests.get(csv_url)

    # Create directory if it doesn't exist
    os.makedirs("intermediate_content", exist_ok=True)
    
    # Write directly to file
    with open("intermediate_content/transfer_player_career_wicks.csv", "wb") as f:
        f.write(response.content)

    # Create the CSV export URL
    csv_url = f"https://docs.google.com/spreadsheets/d/{snap_sheet_id}/export?format=csv&gid={snap_gid}"

    # Read directly into pandas from sheets
    df = pd.read_csv(csv_url)

    return(df)

def make_moved_up_df(transfer_player_snap_counts):

    moved_up_df = transfer_player_snap_counts[
        (
            (transfer_player_snap_counts["prev_level"] == "FCS") &
            (transfer_player_snap_counts["current_level"].isin(["Power Four", "Group of Six"]))
        )
        |
        (
            (transfer_player_snap_counts["prev_level"] == "Group of Six") &
            (transfer_player_snap_counts["current_level"] == "Power Four")
        )
    ]

    succeeded_df = moved_up_df[
        (moved_up_df["current_def_snaps"] > 100) |
        (moved_up_df["current_off_snaps"] > 100)
    ]

    succeeded_df.to_csv("./intermediate_content/succeeded.csv", index=False)

    # succeeded_df

    return succeeded_df

def filter_for_successful():
    import duckdb
    import pandas as pd
    import requests

    #### Initial query to get a sense of successful positions
    query_1 = duckdb.query("""

    SELECT prev_position, count(*) count
    FROM "intermediate_content/succeeded.csv"
    GROUP BY prev_position
    ORDER BY count
    """).to_df()

    # query_1

    #### given successful positions, use create df with all other important information
    succeeded_expanded_df_raw = duckdb.query("""

    SELECT wicks.pff_player_id, player_name, prev_season, current_season, wick_score, capped_wick_score, prev_position, current_pos, prev_school, current_school, prev_def_snaps, current_def_snaps, prev_off_snaps, current_off_snaps
    FROM "intermediate_content/transfer_player_career_wicks.csv" wicks JOIN "intermediate_content/succeeded.csv" succeeded ON wicks.pff_player_id = succeeded.pff_player_id
    WHERE current_pos = prev_position
    """).to_df()

    # succeeded_expanded_df_raw

    succeeded_expanded_df = duckdb.query("""

    SELECT pff_player_id, player_name, prev_season, current_season, prev_position, current_pos, prev_school, current_school, 
            round(avg(wick_score), 1) wick_score, round(avg(capped_wick_score), 1) capped_wick_score, avg(prev_def_snaps) prev_def_snaps, 
            avg(current_def_snaps) current_def_snaps, avg(prev_off_snaps) prev_off_snaps, avg(current_off_snaps) current_off_snaps
    FROM succeeded_expanded_df_raw
    GROUP BY pff_player_id, player_name, prev_season, current_season, prev_position, current_pos, prev_school, current_school
    """).to_df()

    # succeeded_expanded_df

    #### further filter for successful players within these positions, create temp scvs for easy access
    succeeded_def_df = succeeded_expanded_df[(succeeded_expanded_df["current_def_snaps"] > succeeded_expanded_df["current_off_snaps"])]
    succeeded_def_df.to_csv("intermediate_content/succeeded_def.csv", index=False)

    succeeded_off_df = succeeded_expanded_df[(succeeded_expanded_df["current_def_snaps"] < succeeded_expanded_df["current_off_snaps"])]
    succeeded_off_df.to_csv("intermediate_content/succeeded_off.csv", index=False)

    succeeded_expanded_df.to_csv("intermediate_content/succeeded_expanded.csv", index=False)

    succeeded_concat_df = pd.concat([succeeded_off_df, succeeded_def_df], ignore_index=True)
    succeeded_concat_df.to_csv("intermediate_content/succeeded_concat.csv", index=False)


    positions_df = succeeded_expanded_df["current_pos"].isin(["LB", "CB", "WR", "ED"])
    filtered = succeeded_expanded_df[positions_df]
    # filtered

    return filtered

def final_position_selection(succeeded_expanded_df):
    import duckdb

    #### group by position success
    query = duckdb.query("""

    SELECT prev_position prev, count(*) count1
    FROM succeeded_expanded_df
    GROUP BY prev
    ORDER BY count1
    """).to_df()

    query_1 = duckdb.query("""

    SELECT prev_position, count(*) count
    FROM "intermediate_content/succeeded.csv"
    GROUP BY prev_position
    ORDER BY count
    """).to_df()
    # query_1

    # query

    #### organize by success if position remains the same
    query_2 = duckdb.query("""

    SELECT prev, count1, count1/count rate
    FROM query JOIN query_1 ON query.prev = query_1.prev_position
    ORDER BY count1
    """).to_df()

    # query_2

    #### establish the list of ids that I need to add to csv
    positions = ["WR", "LB", "ED", "CB"]

    succeeded_ids_df = succeeded_expanded_df[["pff_player_id", "player_name", "prev_season"]][succeeded_expanded_df["prev_position"].isin(positions)]
    # succeeded_ids_df = succeeded_ids_df[succeeded_expanded_df["prev_position"].isin(positions)]

    # return ids
    succeeded_ids_df.to_csv("intermediate_content/succeeded_ids.csv", index=False)

    # succeeded_ids_df
