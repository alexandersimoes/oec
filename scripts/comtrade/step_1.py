# -*- coding: utf-8 -*-
"""
    Clean raw SECEX data and output to TSV
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The script is the first step in adding a new year of SECEX data to the 
    database. The script will output 1 bzipped TSV file that can then be 
    consumed by step 2 for created the disaggregate tables.

"""


''' Import statements '''
import csv, sys, os, argparse, MySQLdb, time, bz2
import pandas as pd
import numpy as np

from decimal import Decimal, ROUND_HALF_UP
from ..config import DATA_DIR
from ..helpers import get_file
from scripts import YEAR
from os import environ

from cStringIO import StringIO

from ..growth_lib import growth

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["OEC_DB_USER"], 
                        passwd=environ["OEC_DB_PW"], 
                        db=environ["OEC_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

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
    yop_exports_rca = growth.rca(yop_exports)
    yop_exports_rca = pd.DataFrame(yop_exports_rca.stack(), columns=["export_rca"])
    
    yop_imports = yop[["import_val"]]
    yop_imports = yop_imports.reset_index()
    yop_imports = yop_imports.pivot(index="origin_id", columns="sitc_id", values="import_val")
    yop_imports_rca = growth.rca(yop_imports)
    yop_imports_rca = pd.DataFrame(yop_imports_rca.stack(), columns=["import_rca"])
    
    yop_rcas = yop_exports_rca.join(yop_imports_rca)
    
    yop = yop.join(yop_rcas, how="outer")
    yop = yop.replace(0, np.nan)
    yop = yop.dropna(how="all")
    
    return yop

def main(year):
    
    '''Open CSV file'''
    raw_file_path = os.path.abspath(os.path.join(DATA_DIR, 'comtrade', 'comtrade_{0}.csv'.format(year)))
    raw_file = get_file(raw_file_path)
    
    '''This is a HUGE bug on the part of COMTRADE, they have quotes inside 
        quotes which fucks up the CSV reading!!! So we replace all instances of
        the word "improved" with double quotes to 'improved' with single quotes.
        Maybe they should have used tabs...  '''
    raw_file = raw_file.read()
    raw_file = StringIO(raw_file.replace('"improved"', "'improved'"))
    
    comtrade = pd.read_csv(raw_file, sep=',')
    
    crit_drop_wld = comtrade['Partner'] != 'World'
    crit_sitc4 = comtrade['Commodity Code'].str.len()==7
    crit_exports = comtrade['Trade Flow'] == 'Export'
    crit_imports = comtrade['Trade Flow'] == 'Import'
    
    exports = comtrade[crit_drop_wld & crit_sitc4 & crit_exports]
    imports = comtrade[crit_drop_wld & crit_sitc4 & crit_imports]
    
    exports = exports[['Reporter', 'Partner', 'Commodity Code', 'Trade Value']]
    exports.columns = ['origin_id', 'destination_id', 'sitc_id', 'export_val']
    exports = exports.set_index(['origin_id', 'destination_id', 'sitc_id'])
    
    imports = imports[['Reporter', 'Partner', 'Commodity Code', 'Trade Value']]
    imports.columns = ['origin_id', 'destination_id', 'sitc_id', 'import_val']
    imports = imports.set_index(['origin_id', 'destination_id', 'sitc_id'])
    
    yodp = exports.join(imports, how='outer')
    
    yodp = yodp.reset_index(level=['origin_id', 'destination_id', 'sitc_id'])

    country_lookup = get_country_lookup()
    sitc_lookup = get_sitc_lookup()
    
    yodp["origin_id"].replace(country_lookup, inplace=True)
    yodp["destination_id"].replace(country_lookup, inplace=True)
    yodp["sitc_id"].replace(sitc_lookup, inplace=True)
    
    # need to aggregate on duplicate indexes
    yodp.groupby(yodp.index).sum()
    
    yodp = yodp.set_index(['origin_id', 'destination_id', 'sitc_id'])
    
    missing_sitc = set([])
    for sitc in yodp.index.get_level_values(2):
        if 'S2-' in sitc: missing_sitc.add(sitc)
    
    missing_countries = set([])
    for c in yodp.index.get_level_values(0):
        if len(c) > 5: missing_countries.add(c)
    for c in yodp.index.get_level_values(1):
        if len(c) > 5: missing_countries.add(c)
        
    # print yodp.head()
    print; print
    print missing_sitc
    print; print
    print missing_countries
    # sys.exit()
    
    yod = yodp.groupby(level=['origin_id','destination_id']).sum()
    
    yop = yodp.groupby(level=['origin_id','sitc_id']).sum()
    yop = calc_rca(yop)
    
    ydp = yodp.groupby(level=['destination_id','sitc_id']).sum()
    
    yo = yodp.groupby(level=['origin_id']).sum()
    yd = yodp.groupby(level=['destination_id']).sum()
    yp = yodp.groupby(level=['sitc_id']).sum()
    
    # print yo["export_val"].order()
    
    secex_dir = os.path.abspath(os.path.join(DATA_DIR, 'comtrade'))
    if not os.path.exists(secex_dir): os.makedirs(secex_dir)
    new_dir = os.path.abspath(os.path.join(DATA_DIR, 'comtrade', year))
    if not os.path.exists(new_dir): os.makedirs(new_dir)
    
    for new_file in ['yodp', 'yod', 'yop', 'ydp', 'yo', 'yd', 'yp']:
        current_table = eval(new_file)
        current_table = current_table.reset_index()
        current_table["year"] = year
        cols = current_table.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        current_table = current_table[cols]
        new_file_path = os.path.abspath(os.path.join(new_dir, new_file+".tsv.bz2"))
        print ' writing file: ', new_file_path
        current_table.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep="\t", index=False)

if __name__ == "__main__":
    start = time.time()
    
    main(YEAR)
    
    total_run_time = (time.time() - start) / 60
    print; print;
    print "Total runtime: {0} minutes".format(int(total_run_time))
    print; print;