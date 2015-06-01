import sys, os
import pandas as pd
import numpy as np

file_path = os.path.dirname(os.path.realpath(__file__))
ps_calcs_lib_path = os.path.abspath(os.path.join(file_path, "../../../lib/ps_calcs"))
sys.path.insert(0, ps_calcs_lib_path)
import ps_calcs

def calc_rca(yop, hs_id_col, hs_id_lens):
    for tf in ['export', 'import']:
        rcas = pd.DataFrame([])
        for hs_id_len in hs_id_lens:
            yop_rca = yop[["{0}_val".format(tf)]]
            yop_rca = yop_rca.reset_index()
            yop_rca = yop_rca[yop_rca[hs_id_col].str.len() == hs_id_len]
            yop_rca = yop_rca.pivot(index="origin_id", columns=hs_id_col, values="{0}_val".format(tf))
            yop_rca = ps_calcs.rca(yop_rca)
            yop_rca = pd.DataFrame(yop_rca.stack(), columns=["rca"])
            rcas = pd.concat([rcas, yop_rca])
    
        yop["{0}_rca".format(tf)] = rcas["rca"]
    
    yop = yop.replace(0, np.nan)
    
    return yop
