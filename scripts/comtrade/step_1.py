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

from decimal import Decimal, ROUND_HALF_UP
from ..config import DATA_DIR
from ..helpers import get_file
from scripts import YEAR

def main(year):
    
    '''Open CSV file'''
    raw_file_path = os.path.abspath(os.path.join(DATA_DIR, 'comtrade', 'comtrade_{0}.csv'.format(year)))
    raw_file = get_file(raw_file_path)
    
    comtrade = pd.read_csv(raw_file, sep=',')
    
    crit_drop_wld = comtrade['Partner'] != 'World'
    crit_sitc4 = comtrade['Commodity Code'].str.len()==7
    crit_exports = comtrade['Trade Flow'] == 'Export'
    crit_imports = comtrade['Trade Flow'] == 'Import'
    
    exports = comtrade[crit_drop_wld & crit_sitc4 & crit_exports]
    imports = comtrade[crit_drop_wld & crit_sitc4 & crit_imports]
    
    exports = exports[['Reporter', 'Partner', 'Commodity Code', 'Trade Value']]
    exports.columns = ['origin_id', 'destination_id', 'hs_id', 'export_val']
    exports = exports.set_index(['origin_id', 'destination_id', 'hs_id'])
    
    imports = imports[['Reporter', 'Partner', 'Commodity Code', 'Trade Value']]
    imports.columns = ['origin_id', 'destination_id', 'hs_id', 'import_val']
    imports = imports.set_index(['origin_id', 'destination_id', 'hs_id'])
    
    yodp = exports.join(imports, how='outer')
    # print yodp[yodp['export_val'].notnull()]

    yod = yodp.groupby(level=['origin_id','destination_id']).sum()
    yop = yodp.groupby(level=['origin_id','hs_id']).sum()
    ydp = yodp.groupby(level=['destination_id','hs_id']).sum()
    
    yo = yodp.groupby(level=['origin_id']).sum()
    yd = yodp.groupby(level=['destination_id']).sum()
    yp = yodp.groupby(level=['hs_id']).sum()
    
    print yo["export_val"].order()

if __name__ == "__main__":
    start = time.time()
    
    main(YEAR)
    
    total_run_time = (time.time() - start) / 60
    print; print;
    print "Total runtime: {0} minutes".format(int(total_run_time))
    print; print;