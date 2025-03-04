import pandas as pd
from typing import List


def main(
    lst_resp: List[dict],
    selected_cols: list = ["ad_id", "date_start", "spend", "cpc", "cpm", "ctr"],
):
    # retrieve variables, resources, states using the wmill client
    assert lst_resp, "No data"

    df_original = pd.DataFrame(lst_resp)

    # df_selected_columns = df_original.loc[:, df_original.columns.isin(selected_cols)]
    df_selected_columns = df_original.reindex(columns=selected_cols)

    return df_selected_columns.to_dict(orient="records")
