# compute_growth.py
# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    python scripts/common/growth_calc.py \
        data/baci/2012/hs92_yp.tsv.bz2 \
        data/baci/2011/hs92_yp.tsv.bz2 \
        --years=1 \
        --cols=export_val,import_val \
        --strcasts=hs92_id \
        -o data/baci/2012

"""

''' Import statements '''
import os, sys, time, bz2, click
import pandas as pd
import numpy as np
import re

def parse_table_name(t):
    pattern = re.compile('(\w+).tsv(.bz2)*')
    m = pattern.search(t)
    if m:
        return m.group(1)
         
def do_growth(t_name, tbl, tbl_prev, cols, years_ago=1, revision=92):
    '''Growth rate'''
    pk_lookup = {"o": "origin_id", "d": "dest_id", "p": "hs{}_id".format(revision)}
    t_namelook = t_name.split("_")[1]
    pk = [pk_lookup[letter] for letter in t_namelook if letter != 'y']

    tbl = pd.merge(tbl, tbl_prev[pk + cols], how='left', left_on=pk, right_on=pk )
    
    for orig_col_name in cols:
        print "DOING", orig_col_name
        
        # percent growth
        new_col_name = orig_col_name + "_growth_pct"
        if years_ago > 1:
            new_col_name = "{0}_{1}".format(new_col_name, years_ago)
        tbl[new_col_name] = ((1.0 * tbl[orig_col_name+"_x"]) / (1.0*tbl[orig_col_name + "_y"])) ** (1.0/years_ago) - 1
        
        # percent growth
        new_col_name = orig_col_name + "_growth_val"
        if years_ago > 1:
            new_col_name = "{0}_{1}".format(new_col_name, years_ago)
        tbl[new_col_name] = tbl[orig_col_name+"_x"] - tbl[orig_col_name + "_y"]
    for colname in cols:
        del tbl[colname + "_y"]
        tbl.rename(columns={ c+"_x" : c for c in cols }, inplace=True)
        # tbl[new_col_name] = tbl3[new_col_name] # -- this is safe because of the left merge
    return tbl

@click.command()
@click.argument('original_file', type=click.Path(exists=True))
@click.argument('growth_file', type=click.Path(exists=True))
@click.option('-c', '--cols', prompt='Columns separated by commas to compute growth', type=str, required=True)
@click.option('-y', '--years', prompt='years between data points', type=int, required=False, default=1)
@click.option('-s', '--strcasts', type=str, required=False)
@click.option('-r', '--revision', help='HS Revision', type=click.Choice(['92', '96', '02', '07']), default='92')
@click.option('output_path', '--output', '-o', help='Path to save files to.', type=click.Path(), required=True, prompt="Output path")
def main(original_file, growth_file, cols, output_path, revision, years, strcasts):
    start = time.time()
    
    converters = {}
    if strcasts:
        strcastlist = strcasts.split(",")
        converters = {x:str for x in strcastlist}
    
    og_df = pd.read_csv(original_file, sep="\t", converters=converters, compression="bz2", na_values=['\N', None])
    growth_df = pd.read_csv(growth_file, sep="\t", converters=converters, compression="bz2", na_values=['\N', None])

    col_names = cols.split(",")
    print "CALCULATING growth for the following columns:", col_names
    
    t_name = parse_table_name(original_file)

    new_df = do_growth(t_name, og_df, growth_df, col_names, years, revision)
    
    
    print "GOT TABLE NAME OF", t_name
    if not t_name:
        t_name = "noname"
    new_file_path = os.path.abspath(os.path.join(output_path, "{0}.tsv.bz2".format(t_name)))
    new_df.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep="\t", index=False, float_format="%.3f", na_rep="\N")
    
    print("--- %s minutes ---" % str((time.time() - start)/60))

if __name__ == "__main__":
    main()
    