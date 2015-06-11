# compute_growth.py
# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    PCI --
    python scripts/baci/rank_delta.py \
        data/baci/1996/hs92_yp.tsv.bz2 \
        data/baci/1995/hs92_yp.tsv.bz2 \
        --rank_col=pci_rank \
        --index_cols=hs92_id \
        --strcasts=hs92_id \
        -o data/baci/2012

"""

''' Import statements '''
import os, sys, time, bz2, click
import pandas as pd
import re

def parse_table_name(t):
    pattern = re.compile('(\w+).tsv(.bz2)*')
    m = pattern.search(t)
    if m:
        return m.group(1)

@click.command()
@click.argument('original_file', type=click.Path(exists=True))
@click.argument('prev_year_file', type=click.Path(exists=True))
@click.option('-s', '--strcasts', type=str, required=False)
@click.option('-c', '--rank_col', prompt='Columns separated by commas to compute growth', type=str, required=True)
@click.option('-i', '--index_cols', prompt='Columns separated by commas to compute growth', type=str, required=True)
@click.option('output_path', '--output', '-o', help='Path to save files to.', type=click.Path(), required=True, prompt="Output path")
def main(original_file, prev_year_file, strcasts, rank_col, index_cols, output_path):
    start = time.time()
    
    converters = {}
    if strcasts:
        strcastlist = strcasts.split(",")
        converters = {x:str for x in strcastlist}
    
    index_cols = index_cols.split(",")
    
    og_df = pd.read_csv(original_file, sep="\t", converters=converters, compression="bz2", na_values=['\N', None])
    prev_year_df = pd.read_csv(prev_year_file, sep="\t", converters=converters, compression="bz2", na_values=['\N', None])
    
    og_df = og_df.set_index(index_cols)
    prev_year_df = prev_year_df.set_index(index_cols)
    
    print "CALCULATING rank delta for:", rank_col
    
    og_df["{}_delta".format(rank_col)] = prev_year_df[rank_col] - og_df[rank_col]
    
    '''re-order so rank_delta column is immediately after rank column'''
    og_df_cols = og_df.columns.tolist()
    rank_col_index = og_df_cols.index(rank_col)+1
    og_df_cols = og_df_cols[:rank_col_index] + ["{}_delta".format(rank_col)] + og_df_cols[rank_col_index:-1]
    og_df = og_df[og_df_cols]
    
    '''reset index'''
    og_df = og_df.reset_index()
    og_df = og_df.set_index(["year"]+index_cols)
    
    t_name = parse_table_name(original_file)
    print "GOT TABLE NAME OF", t_name
    if not t_name:
        t_name = "noname"
    new_file_path = os.path.abspath(os.path.join(output_path, "{0}.tsv.bz2".format(t_name)))
    og_df.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep="\t", index=True, float_format="%.3f", na_rep="\N")
    
    print("--- %s minutes ---" % str((time.time() - start)/60))

if __name__ == "__main__":
    main()
    