import sys, os
import pandas as pd
import numpy as np

file_path = os.path.dirname(os.path.realpath(__file__))
ps_calcs_lib_path = os.path.abspath(os.path.join(file_path, "../../../lib/ps_calcs"))
sys.path.insert(0, ps_calcs_lib_path)
import ps_calcs

def calc_rca(yop):
    for tf in ['export', 'import']:
        yop_rca = yop[["{0}_val".format(tf)]]
        yop_rca = yop_rca.reset_index()
        yop_rca = yop_rca.pivot(index="origin_id", columns="hs_id", values="{0}_val".format(tf))
        yop_rca = ps_calcs.rca(yop_rca)
        yop_rca = pd.DataFrame(yop_rca.stack(), columns=["rca"])
        yop["{0}_rca".format(tf)] = yop_rca["rca"]
    
    yop = yop.replace(0, np.nan)
    
    return yop
