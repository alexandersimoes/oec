def calc_top_prod_dest(yo, yp, yop, yod):
    '''top export/import & top dest/origin'''
    for tf in ['export', 'import']:
        yp_top = yop.fillna(0).groupby(level=["hs_id"])["{0}_val".format(tf)].apply(lambda x: x.idxmax()[0])
        yo_top_prod = yop.fillna(0).groupby(level=["origin_id"])["{0}_val".format(tf)].apply(lambda x: x.idxmax()[1])
        yo_top_dest = yod.fillna(0).groupby(level=["origin_id"])["{0}_val".format(tf)].apply(lambda x: x.idxmax()[1])
        yo["top_{0}".format(tf)] = yo_top_prod
        yo["top_{0}_dest".format(tf)] = yo_top_dest
        yp["top_{0}er".format(tf)] = yp_top
    
    return (yo, yp)
