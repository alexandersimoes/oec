# -*- coding: utf-8 -*-
"""
    Format COMTRADE data for DB entry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Example Usage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    python scripts/comtrade/format_data.py data/comtrade/comtrade_2014.csv -y 2014 -o data/comtrade/

"""

''' Import statements '''
import csv, sys, os, argparse, MySQLdb, time, click, bz2
import pandas as pd
import numpy as np

from decimal import Decimal, ROUND_HALF_UP
from os import environ
from helpers.import_file import import_file

file_path = os.path.dirname(os.path.realpath(__file__))
ps_calcs_lib_path = os.path.abspath(os.path.join(file_path, "../../lib/ps_calcs"))
sys.path.insert(0, ps_calcs_lib_path)
import ps_calcs

def get_country_lookup():
    cursor.execute("select comtrade_name, id from attr_country where comtrade_name is not null;")
    cs = {}
    for c in cursor.fetchall():
        c_list, c_id = c
        for c in c_list.split("|"):
            cs[c.strip()] = c_id
    return cs

def get_sitc_lookup():
    cursor.execute("select concat('S2-', sitc), id from attr_sitc;")
    return {c[0]:c[1] for c in cursor.fetchall()}

def calc_rca(yop):
    
    yop_exports = yop[["export_val"]]
    yop_exports = yop_exports.reset_index()
    yop_exports = yop_exports.pivot(index="origin_id", columns="sitc_id", values="export_val")
    yop_exports_rca = ps_calcs.rca(yop_exports)
    yop_exports_rca = pd.DataFrame(yop_exports_rca.stack(), columns=["export_rca"])
    
    yop_imports = yop[["import_val"]]
    yop_imports = yop_imports.reset_index()
    yop_imports = yop_imports.pivot(index="origin_id", columns="sitc_id", values="import_val")
    yop_imports_rca = ps_calcs.rca(yop_imports)
    yop_imports_rca = pd.DataFrame(yop_imports_rca.stack(), columns=["import_rca"])
    
    yop_rcas = yop_exports_rca.join(yop_imports_rca)
    
    yop = yop.join(yop_rcas, how="outer")
    yop = yop.replace(0, np.nan)
    yop = yop.dropna(how="all")
    
    return yop

def calc_top_prod_dest(yo, yp, yop, yod):
    '''top export/import & top dest/origin'''
    for tf in ['export', 'import']:
        yp_top_origin = yop.fillna(0).groupby(level=["sitc_id"])["{0}_val".format(tf)].apply(lambda x: x.idxmax()[0])
        
        this_yop = yop.reset_index()
        this_yop = this_yop[this_yop["sitc_id"].str.len() == 6]
        this_yop = this_yop.set_index(["origin_id", "sitc_id"])
        yo_top_prod_sitc = this_yop.fillna(0).groupby(level=["origin_id"])["{0}_val".format(tf)].apply(lambda x: x.idxmax()[1])
        
        yo_top_dest = yod.fillna(0).groupby(level=["origin_id"])["{0}_val".format(tf)].apply(lambda x: x.idxmax()[1])
        
        yo["top_{}".format(tf)] = yo_top_prod_sitc
        yo["top_{}_dest".format(tf)] = yo_top_dest
        yp["top_{}er".format(tf)] = yp_top_origin
    
    return (yo, yp)

def calc_id_len(table_name, table_data):
    indicies = [('p', 'sitc_id')]
    for index, column in indicies:
        if index in table_name:
            table_data.loc[:, column + "_len"] = table_data.reset_index()[column].str.len().tolist()
            cols = table_data.columns.tolist()
            cols = [column + "_len"] + cols[:-1]
            table_data = table_data[cols]
    return table_data

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-y', '--year', prompt='Year', help='year of the data to convert', required=True, type=int)
@click.option('-o', '--output_dir', help='output directory', type=click.Path(), default="data/baci")
def main(input_file, year, output_dir):
    
    output_dir = os.path.abspath(os.path.join(output_dir, str(year)))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    store = pd.HDFStore(os.path.join(output_dir,'comtrade_yodp.h5'))
    
    try:
        yodp = store.get('yodp')
    except KeyError:
        '''
        STEP 1:
        Import file to pandas dataframe.'''
        yodp = import_file(input_file)
        
        store.put('yodp', yodp)
    
    yod = yodp.groupby(level=['origin_id','dest_id']).sum()
    yop = yodp.groupby(level=['origin_id','sitc_id']).sum()
    ydp = yodp.groupby(level=['dest_id','sitc_id']).sum()
    yo = yodp.groupby(level=['origin_id']).sum()
    yd = yodp.groupby(level=['dest_id']).sum()
    yp = yodp.groupby(level=['sitc_id']).sum()
    
    ''' Calculate RCA '''
    yop = calc_rca(yop)
    
    ''' Calculate top product and destination '''
    yo, yp = calc_top_prod_dest(yo, yp, yop, yod)
    
    # print yo["export_val"].order()
    tables = {"yodp":yodp, "yop":yop, "yod":yod, "ydp":ydp, "yo":yo, "yp":yp, "yd":yd}
    
    ''' Calculate HS ID len '''
    for tname, table in tables.items():
        if "p" in tname:
            tables[tname] = calc_id_len(tname, table)
    
    for df in tables.items():
        name, data = df
        
        '''reorder columns so year is first'''
        data = data.reset_index()
        data["year"] = year
        cols = data.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        data = data[cols]
        
        '''create new BZ2 formatted file'''
        new_file_path = os.path.abspath(os.path.join(output_dir, "sitc_{}.tsv.bz2".format(name)))
        print ' writing file: ', name
        data.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep="\t", index=False, na_rep="\N")

if __name__ == "__main__":
    start = time.time()

    main()
    
    total_run_time = (time.time() - start) / 60
    print; print;
    print "Total runtime: {0} minutes".format(int(total_run_time))
    print; print;