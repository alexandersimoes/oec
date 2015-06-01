import sys, os
import pandas as pd

def aggregate(baci_df, hs_id_col):
    
    ''' PRODUCTS '''
    baci_hs4 = baci_df.copy()
    baci_hs4[hs_id_col] = baci_hs4[hs_id_col].str.slice(0, 6)
    baci_hs4 = baci_hs4.groupby(["origin_id", "dest_id", hs_id_col]).sum()
    
    baci_df = pd.concat([baci_df, baci_hs4.reset_index()])
    
    return baci_df
    