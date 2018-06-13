# -*- coding: utf-8 -*-
"""
    Format BACI data for DB entry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Example Usage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    python scripts/baci/format_data.py data/baci/baci92_2012.rar -y 2012 -o data/baci/ -r 92

"""

''' Import statements '''
import os, sys, time, MySQLdb, click
import pandas as pd
import pandas.io.sql as sql
import numpy as np
from helpers.import_file import import_file
from helpers.calc_rca import calc_rca
from helpers.calc_top_prod_dest import calc_top_prod_dest
from helpers.calc_complexity import calc_complexity
from helpers.write_to_files import write_to_files
from helpers.get_attr_yo import get_attr_yo
from helpers.calc_id_len import calc_id_len
from helpers.aggregate import aggregate

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=os.environ["OEC_DB_USER"],
                        passwd=os.environ["OEC_DB_PW"],
                        db=os.environ["OEC_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def add_index(baci_df, hs_id_col):
    baci_df = baci_df.set_index(["origin_id", "dest_id", hs_id_col])
    baci_df = baci_df.groupby(level=['origin_id', 'dest_id', hs_id_col]).sum()

    baci_df_import = baci_df.copy()
    baci_df_import.columns = ['import_val']
    baci_df_import = baci_df_import.swaplevel('origin_id', 'dest_id')
    baci_df_import.index.names = ['origin_id', 'dest_id', hs_id_col]

    baci_df = pd.merge(baci_df, baci_df_import, right_index=True, left_index=True, how='outer')

    return baci_df

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-y', '--year', prompt='Year', help='year of the data to convert', required=True, type=int)
@click.option('-o', '--output_dir', help='output directory', type=click.Path(), default="data/baci")
@click.option('-r', '--hs_revision', help='HS Revision', type=click.Choice(['92', '96', '02', '07']), default='92')
def main(input_file, year, output_dir, hs_revision):
    hs_id_col = "hs{}_id".format(hs_revision)
    hs_id_lens = [6, 8]
    attr_yo = get_attr_yo(year)

    output_dir = os.path.abspath(os.path.join(output_dir, str(year)))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    store = pd.HDFStore(os.path.join(output_dir,'yodp{}.h5'.format(hs_revision)))

    try:
        yodp = store.get('yodp')
    except KeyError:
        '''
        STEP 1:
        Import file to pandas dataframe.'''
        baci_df = import_file(input_file, hs_id_col)

        '''
        STEP 2:
        Aggregate diff levels of depth.'''
        baci_df = aggregate(baci_df, hs_id_col)

        '''
        STEP 3:
        Add indexes'''
        yodp = add_index(baci_df, hs_id_col)

        store.put('yodp', yodp)

    '''
    STEP 4:
    Aggregate'''
    yop = yodp.groupby(level=['origin_id',hs_id_col]).sum()
    ydp = yodp.groupby(level=['dest_id',hs_id_col]).sum()
    yp = yodp.groupby(level=[hs_id_col]).sum()

    # need to set a specific HS depth for aggregations without hsxx_id
    yodp_no_index = yodp.reset_index()
    yodp_no_index = yodp_no_index[yodp_no_index[hs_id_col].str.len() == hs_id_lens[0]]
    yod = yodp_no_index.groupby(['origin_id','dest_id']).sum()
    yo = yodp_no_index.groupby(['origin_id']).sum()
    yd = yodp_no_index.groupby(['dest_id']).sum()

    '''
    STEP 5:
    Calculate RCA'''
    yop = calc_rca(yop, hs_id_col, hs_id_lens)

    '''
    STEP 6:
    Calculate top product and destination'''
    yo, yp = calc_top_prod_dest(yo, yp, yop, yod, hs_id_col)

    '''
    STEP 7:
    Calculate complexity'''
    attr_yo, yp = calc_complexity(attr_yo, yp, yop, year, hs_id_col, hs_id_lens)

    tables = {"yodp":yodp, "yop":yop, "yod":yod, "ydp":ydp, "yo":yo, "yp":yp, "yd":yd}

    '''
    STEP 8:
    Calculate HS ID len'''
    for tname, table in tables.items():
        if "p" in tname:
            tables[tname] = calc_id_len(tname, table, hs_id_col)

    '''
    STEP 9:
    Write out to files'''
    tables["attr_yo"] = attr_yo
    write_to_files(year, tables.items(), output_dir, hs_revision)

if __name__ == "__main__":
    start = time.time()

    main()

    total_run_time = (time.time() - start) / 60
    print; print;
    print "Total runtime: {0} minutes".format(int(total_run_time))
    print; print;
