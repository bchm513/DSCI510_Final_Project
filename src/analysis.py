##### This is the file where I create all of the results/visuals for my analysis. 
# I have already considered using other models including logistic regressions and different forms of linear regressions, but have settled on a LassoCV and RandomForest model for my "business" needs

def get_columns():
    #### get columns for data analysis
    import pandas as pd
    import json

    column_list = []

    with open("../data/season_grades_filtered.json", "r") as fin:
        data = json.load(fin)

    season_grades_filtered_df = pd.DataFrame(data)
    # season_grades_filtered_df

    for entry in data:
        for key in entry:
            # print(key)
            if key not in column_list:
                column_list.append(key)
        # break
    # season_grades_filtered_df

    return column_list

def get_agg_dict():
    #### get aggregated dictionary of stats for analysis
    import duckdb
    import pandas as pd
    import json

    with open("../data/season_grades_filtered.json", "r") as fin:
        data = json.load(fin)

    season_grades_filtered_df = pd.DataFrame(data)

    agg_dict = {
        "position": "first",
        "unit": "first",
        "player": "first",

        "run_defense_snaps": "sum",
        "pass_rush_snaps": "sum",
        "coverage_snaps": "sum",
        "total_snaps": "sum",
        "run_block_snaps": "sum",
        "receiving_snaps": "sum",
        "pass_block_snaps": "sum",
        "run_snaps": "sum",
        "pass_snaps": "sum",

        "run_defense": "mean",
        "pass_rush": "mean",
        "coverage": "mean",
        "discipline": "mean",
        "defense": "mean",
        "run_block": "mean",
        "receiving": "mean",
        "pass_block": "mean",
        "run": "mean",
        "pass": "mean",
        "offense": "mean",

        "coverage_rank": "mean",
        "offense_rank": "mean",
        "defense_rank": "mean",
        "run_defense_rank": "mean",
        "pass_rush_rank": "mean",
        "receiving_rank": "mean",
        "pass_rank": "mean",
        "run_block_rank": "mean",
        "pass_block_rank": "mean",
        "run_rank": "mean"
    }

    df_agg = season_grades_filtered_df.groupby(["player_id", "season"]).agg(agg_dict).reset_index().sort_values(["position", "season"])

    wick_combine = duckdb.query("""

    SELECT *
    FROM df_agg JOIN "intermediate_content/transfer_player_career_wicks.csv" wicks ON df_agg.player_id = wicks.pff_player_id AND df_agg.season = wicks.season
    ORDER BY df_agg.position
    """).to_df()


    # df_agg.to_csv("agged_season_stats.csv", index=False)
    wick_combine.to_csv("clean_data/agged_season_stats.csv", index=False)

# broad analysis considering all positions
def total_analysis():
    import pandas as pd

    from sklearn.model_selection import train_test_split
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LassoCV
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import plot_tree

    import matplotlib.pyplot as plt

    tot = pd.read_csv('clean_data/agged_season_stats.csv')

    drop_cols = [
        'index', 'player_id', 'player', 'pff_player_id', 'position', 'unit',
        'season_1', 'position_1', 'season',
        'coverage_rank', 'offense_rank', 'defense_rank',
        'run_defense_rank', 'pass_rush_rank', 'receiving_rank',
        'pass_rank', 'run_block_rank', 'pass_block_rank', 'run_rank'
    ]

    tot_clean = tot.drop(columns=[c for c in drop_cols if c in tot.columns])
    # tot_clean

    target_cols = ['wick_score', 'capped_wick_score']
    X = tot_clean.drop(columns=target_cols)
    y = tot_clean[target_cols]

    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)


    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y['wick_score'], test_size=0.2, random_state=42
    )

    # ----------------------
    # Random Forest model
    # ----------------------
    rf = RandomForestRegressor(n_estimators=500, max_depth=4, random_state=42)
    rf.fit(X_train, y_train)

    feature_importance_rf = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    # print("\nTop features by Random Forest:")
    # print(feature_importance_rf)

    plt.figure(figsize=(10, 6))
    feature_importance_rf.plot(kind='bar')
    plt.title("Top Features by Random Forest")
    plt.ylabel("Importance")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(20, 10))
    # Plot the first tree in the forest
    plot_tree(
        rf.estimators_[0],
        feature_names=X.columns,
        filled=True,
        rounded=True,
        fontsize=10
    )
    plt.title("Random Forest - First Tree Visualization")
    plt.show()

    # ----------------------
    # LassoCV model
    # ----------------------
    lasso = LassoCV(cv=5, random_state=42)
    lasso.fit(X_train, y_train)

    # Feature importance
    feature_importance_lasso = pd.Series(lasso.coef_, index=X.columns).sort_values(ascending=False)
    # print("Top features by LassoCV:")
    # print(feature_importance_lasso)

    plt.figure(figsize=(10, 6))
    feature_importance_lasso_abs = feature_importance_lasso.abs().sort_values(ascending=False)
    feature_importance_lasso_abs.plot(kind='bar', color='orange')
    plt.title("Top Features by LassoCV (Absolute Coefficients)")
    plt.ylabel("Coefficient Magnitude")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# analysis for db position
def db_analysis():
    import pandas as pd

    dbs = pd.read_csv('clean_data/dbs.csv')

    from sklearn.model_selection import train_test_split
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LassoCV
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import plot_tree

    import matplotlib.pyplot as plt

    drop_cols = [
        'index', 'player_id', 'player', 'pff_player_id', 'position', 'unit',
        'season_1', 'position_1', 'season',
        'run_block_snaps', 'receiving_snaps', 'pass_block_snaps', 'run_snaps', 'pass_snaps',
        'run_block', 'receiving', 'pass_block', 'run', 'pass', 'offense',
        'pass_rush_rank', 'receiving_rank', 'pass_rank', 'run_block_rank', 'pass_block_rank', 'run_rank',
        'season_1', 'position_1', 'pff_player_id'
    ]

    dbs_clean = dbs.drop(columns=[c for c in drop_cols if c in dbs.columns])
    # tot_clean

    target_cols = ['wick_score', 'capped_wick_score']
    X = dbs_clean.drop(columns=target_cols)
    y = dbs_clean[target_cols]

    X_numeric = X.select_dtypes(include='number')

    # Impute
    imputer = SimpleImputer(strategy='median')
    X_imputed_array = imputer.fit_transform(X_numeric)

    # Only use the columns that were actually imputed
    X_imputed = pd.DataFrame(X_imputed_array, columns=X_numeric.columns[:X_imputed_array.shape[1]])

    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X_imputed), columns=X_imputed.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y['wick_score'], test_size=0.2, random_state=42
    )

    # print(X_numeric.columns)
    # print(X_imputed.columns)
    # print(X_train.columns)

    # ----------------------
    # Random Forest model
    # ----------------------
    rf = RandomForestRegressor(n_estimators=500, max_depth=4, random_state=42)
    rf.fit(X_train, y_train)

    # print(X.columns)
    # print(X_train.columns)

    feature_importance_rf = pd.Series(rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    # print("\nTop features by Random Forest:")
    # print(feature_importance_rf)

    plt.figure(figsize=(10, 6))
    feature_importance_rf.plot(kind='bar')
    plt.title("Top Features by Random Forest")
    plt.ylabel("Importance")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(20, 10))
    # Plot the first tree in the forest
    plot_tree(
        rf.estimators_[0],
        feature_names=X.columns,
        filled=True,
        rounded=True,
        fontsize=10
    )
    plt.title("Random Forest - First Tree Visualization")
    plt.show()

    # ----------------------
    # LassoCV model
    # ----------------------
    lasso = LassoCV(cv=5, random_state=42)
    lasso.fit(X_train, y_train)

    # Feature importance
    feature_importance_lasso = pd.Series(lasso.coef_, index=X_train.columns).sort_values(ascending=False)
    # print("Top features by LassoCV:")
    # print(feature_importance_lasso)

    plt.figure(figsize=(10, 6))
    feature_importance_lasso_abs = feature_importance_lasso.abs().sort_values(ascending=False)
    feature_importance_lasso_abs.plot(kind='bar', color='orange')
    plt.title("Top Features by LassoCV (Absolute Coefficients)")
    plt.ylabel("Coefficient Magnitude")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# analysis for ed position
def ed_analysis():
    import pandas as pd

    eds = pd.read_csv('clean_data/eds.csv')

    from sklearn.model_selection import train_test_split
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LassoCV
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import plot_tree

    import matplotlib.pyplot as plt

    drop_cols = [
        'index', 'player_id', 'player', 'pff_player_id', 'position', 'unit',
        'season_1', 'position_1', 'season',
        'run_block_snaps', 'receiving_snaps', 'pass_block_snaps', 'run_snaps', 'pass_snaps',
        'run_block', 'receiving', 'pass_block', 'run', 'pass', 'offense',
        'pass_rush_rank', 'receiving_rank', 'pass_rank', 'run_block_rank', 'pass_block_rank', 'run_rank',
        'season_1', 'position_1', 'pff_player_id'
    ]

    eds_clean = eds.drop(columns=[c for c in drop_cols if c in eds.columns])
    # tot_clean

    target_cols = ['wick_score', 'capped_wick_score']
    X = eds_clean.drop(columns=target_cols)
    y = eds_clean[target_cols]

    X_numeric = X.select_dtypes(include='number')

    # Impute
    imputer = SimpleImputer(strategy='median')
    X_imputed_array = imputer.fit_transform(X_numeric)

    # Only use the columns that were actually imputed
    X_imputed = pd.DataFrame(X_imputed_array, columns=X_numeric.columns[:X_imputed_array.shape[1]])


    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X_imputed), columns=X_imputed.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y['wick_score'], test_size=0.2, random_state=42
    )

    # print(X_numeric.columns)
    # print(X_imputed.columns)
    # print(X_train.columns)

    # ----------------------
    # Random Forest model
    # ----------------------
    rf = RandomForestRegressor(n_estimators=500, max_depth=4, random_state=42)
    rf.fit(X_train, y_train)

    feature_importance_rf = pd.Series(rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    # print("\nTop features by Random Forest:")
    # print(feature_importance_rf)

    plt.figure(figsize=(10, 6))
    feature_importance_rf.plot(kind='bar')
    plt.title("Top Features by Random Forest")
    plt.ylabel("Importance")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(20, 10))
    # Plot the first tree in the forest
    plot_tree(
        rf.estimators_[0],
        feature_names=X.columns,
        filled=True,
        rounded=True,
        fontsize=10
    )
    plt.title("Random Forest - First Tree Visualization")
    plt.show()

    # ----------------------
    # LassoCV model
    # ----------------------
    lasso = LassoCV(cv=5, random_state=42)
    lasso.fit(X_train, y_train)

    # Feature importance
    feature_importance_lasso = pd.Series(lasso.coef_, index=X_train.columns).sort_values(ascending=False)
    # print("Top features by LassoCV:")
    # print(feature_importance_lasso)

    plt.figure(figsize=(10, 6))
    feature_importance_lasso_abs = feature_importance_lasso.abs().sort_values(ascending=False)
    feature_importance_lasso_abs.plot(kind='bar', color='orange')
    plt.title("Top Features by LassoCV (Absolute Coefficients)")
    plt.ylabel("Coefficient Magnitude")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# analysis for lb position
def lb_analysis():
    import pandas as pd

    lbs = pd.read_csv('clean_data/lbs.csv')

    from sklearn.model_selection import train_test_split
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LassoCV
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import plot_tree

    import matplotlib.pyplot as plt

    drop_cols = [
        'index', 'player_id', 'player', 'pff_player_id', 'position', 'unit',
        'season_1', 'position_1', 'season',
        'run_block_snaps', 'receiving_snaps', 'pass_block_snaps', 'run_snaps', 'pass_snaps',
        'run_block', 'receiving', 'pass_block', 'run', 'pass', 'offense',
        'pass_rush_rank', 'receiving_rank', 'pass_rank', 'run_block_rank', 'pass_block_rank', 'run_rank',
        'season_1', 'position_1', 'pff_player_id'
    ]

    lbs_clean = lbs.drop(columns=[c for c in drop_cols if c in lbs.columns])
    # tot_clean

    target_cols = ['wick_score', 'capped_wick_score']
    X = lbs_clean.drop(columns=target_cols)
    y = lbs_clean[target_cols]

    X_numeric = X.select_dtypes(include='number')

    # Impute
    imputer = SimpleImputer(strategy='median')
    X_imputed_array = imputer.fit_transform(X_numeric)

    # Only use the columns that were actually imputed
    X_imputed = pd.DataFrame(X_imputed_array, columns=X_numeric.columns[:X_imputed_array.shape[1]])


    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X_imputed), columns=X_imputed.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y['wick_score'], test_size=0.2, random_state=42
    )

    # print(X_numeric.columns)
    # print(X_imputed.columns)
    # print(X_train.columns)


    # ----------------------
    # Random Forest model
    # ----------------------
    rf = RandomForestRegressor(n_estimators=500, max_depth=4, random_state=42)
    rf.fit(X_train, y_train)

    feature_importance_rf = pd.Series(rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    # print("\nTop features by Random Forest:")
    # print(feature_importance_rf)

    plt.figure(figsize=(10, 6))
    feature_importance_rf.plot(kind='bar')
    plt.title("Top Features by Random Forest")
    plt.ylabel("Importance")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(20, 10))
    # Plot the first tree in the forest
    plot_tree(
        rf.estimators_[0],
        feature_names=X.columns,
        filled=True,
        rounded=True,
        fontsize=10
    )
    plt.title("Random Forest - First Tree Visualization")
    plt.show()

    # ----------------------
    # LassoCV model
    # ----------------------
    lasso = LassoCV(cv=5, random_state=42)
    lasso.fit(X_train, y_train)

    # Feature importance
    feature_importance_lasso = pd.Series(lasso.coef_, index=X_train.columns).sort_values(ascending=False)
    # print("Top features by LassoCV:")
    # print(feature_importance_lasso)

    plt.figure(figsize=(10, 6))
    feature_importance_lasso_abs = feature_importance_lasso.abs().sort_values(ascending=False)
    feature_importance_lasso_abs.plot(kind='bar', color='orange')
    plt.title("Top Features by LassoCV (Absolute Coefficients)")
    plt.ylabel("Coefficient Magnitude")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# analysis for wr position
def wr_analysis():
    import pandas as pd

    wrs = pd.read_csv('clean_data/wrs.csv')

    from sklearn.model_selection import train_test_split
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LassoCV
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import plot_tree

    import matplotlib.pyplot as plt

    drop_cols = [
        'index', 'player_id', 'player', 'pff_player_id', 'position', 'unit',
        'season_1', 'position_1', 'season', 'pass_rush', 
        'coverage_rank', 'offense_rank', 'defense_rank',
        'run_defense_rank', 'pass_rush_rank', 'receiving_rank',
        'pass_rank', 'run_block_rank', 'pass_block_rank', 'run_rank'
    ]

    wrs_clean = wrs.drop(columns=[c for c in drop_cols if c in wrs.columns])
    # tot_clean

    target_cols = ['wick_score', 'capped_wick_score']
    X = wrs_clean.drop(columns=target_cols)
    y = wrs_clean[target_cols]

    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)


    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y['wick_score'], test_size=0.2, random_state=42
    )

    # ----------------------
    # Random Forest model
    # ----------------------
    rf = RandomForestRegressor(n_estimators=500, max_depth=4, random_state=42)
    rf.fit(X_train, y_train)

    feature_importance_rf = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    # print("\nTop features by Random Forest:")
    # print(feature_importance_rf)

    plt.figure(figsize=(10, 6))
    feature_importance_rf.plot(kind='bar')
    plt.title("Top Features by Random Forest")
    plt.ylabel("Importance")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(20, 10))
    # Plot the first tree in the forest
    plot_tree(
        rf.estimators_[0],
        feature_names=X.columns,
        filled=True,
        rounded=True,
        fontsize=10
    )
    plt.title("Random Forest - First Tree Visualization")
    plt.show()

    # ----------------------
    # LassoCV model
    # ----------------------
    lasso = LassoCV(cv=5, random_state=42)
    lasso.fit(X_train, y_train)

    # Feature importance
    feature_importance_lasso = pd.Series(lasso.coef_, index=X.columns).sort_values(ascending=False)
    # print("Top features by LassoCV:")
    # print(feature_importance_lasso)

    plt.figure(figsize=(10, 6))
    feature_importance_lasso_abs = feature_importance_lasso.abs().sort_values(ascending=False)
    feature_importance_lasso_abs.plot(kind='bar', color='orange')
    plt.title("Top Features by LassoCV (Absolute Coefficients)")
    plt.ylabel("Coefficient Magnitude")
    plt.xlabel("Features")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

