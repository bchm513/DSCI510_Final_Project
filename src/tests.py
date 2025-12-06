#### Example test of retrieving the wick and snap scores from my google drive
#### This will create intermediate_content file outside of src, go to results.ipynb or main for full pipeline

from processing import retrieve_wicks
import config

transfer_player_snap_counts = retrieve_wicks(config.SNAP_COUNTS_GID, config.SNAP_COUNTS_SHEETID, config.WICKS_GID, config.WICKS_SHEETID)
