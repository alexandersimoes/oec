import pandas as pd
import sys

def calc_id_len(table_name, table_data, hs_id_col):
    indicies = [('p', hs_id_col)]
    for index, column in indicies:
        if index in table_name:
            table_data.loc[:, column + "_len"] = table_data.reset_index()[column].str.len().tolist()
            cols = table_data.columns.tolist()
            cols = [column + "_len"] + cols[:-1]
            table_data = table_data[cols]
    return table_data