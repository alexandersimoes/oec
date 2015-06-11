import sys

def calc_top_prod_dest(yo, yp, yop, yod, hs_id_col):
    '''top export/import & top dest/origin'''
    for tf in ['export', 'import']:
        yp_top_origin = yop.fillna(0).groupby(level=[hs_id_col])["{0}_val".format(tf)].apply(lambda x: x.idxmax()[0])
        
        this_yop = yop.reset_index()
        this_yop = this_yop[this_yop[hs_id_col].str.len() == 6]
        this_yop = this_yop.set_index(["origin_id", hs_id_col])
        yo_top_prod = this_yop.fillna(0).groupby(level=["origin_id"])["{0}_val".format(tf)].apply(lambda x: x.idxmax()[1])
        
        yo_top_dest = yod.fillna(0).groupby(level=["origin_id"])["{0}_val".format(tf)].apply(lambda x: x.idxmax()[1])
        
        yo["top_{0}".format(tf)] = yo_top_prod
        yo["top_{0}_dest".format(tf)] = yo_top_dest
        yp["top_{0}er".format(tf)] = yp_top_origin
    
    return (yo, yp)
