''' Import statements '''
import csv, sys, os, argparse, MySQLdb, time, bz2
import pandas as pd
import numpy as np

from decimal import Decimal, ROUND_HALF_UP
from ..config import DATA_DIR
from ..helpers import get_file
from scripts import YEAR
from os import environ

from ..growth_lib import growth

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=environ["OEC_DB_USER"], 
                        passwd=environ["OEC_DB_PW"], 
                        db=environ["OEC_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_country_lookup():
    cursor.execute("select id_num, id from attr_country where id_num is not null;")
    cs = {}
    for c in cursor.fetchall():
        c_list, c_id = c
        for c in str(c_list).split("|"):
            cs[c.strip()] = c_id
    return cs

def get_hs_lookup():
    cursor.execute("select hs_code, id from attr_hs;")
    return {c[0]:c[1] for c in cursor.fetchall()}

def calc_rca(yop):
    
    yop_exports = yop[["export_val"]]
    yop_exports = yop_exports.reset_index()
    yop_exports = yop_exports.pivot(index="origin_id", columns="hs_id", values="export_val")
    yop_exports_rca = growth.rca(yop_exports)
    yop_exports_rca = pd.DataFrame(yop_exports_rca.stack(), columns=["export_rca"])
    
    yop_imports = yop[["import_val"]]
    yop_imports = yop_imports.reset_index()
    yop_imports = yop_imports.pivot(index="origin_id", columns="hs_id", values="import_val")
    yop_imports_rca = growth.rca(yop_imports)
    yop_imports_rca = pd.DataFrame(yop_imports_rca.stack(), columns=["import_rca"])
    
    yop_rcas = yop_exports_rca.join(yop_imports_rca)
    
    yop = yop.join(yop_rcas, how="outer")
    yop = yop.replace(0, np.nan)
    yop = yop.dropna(how="all")
    
    return yop

def main(year):
    
    '''Open CSV file'''
    raw_file_path = os.path.abspath(os.path.join(DATA_DIR, 'baci', 'baci92_{0}.csv'.format(year)))
    raw_file = get_file(raw_file_path)
    
    baci = pd.read_csv(raw_file, sep=',')
    baci = baci[["hs6", "i", "j", "v"]]
    baci.columns = ["hs_id", "origin_id", "destination_id", "export_val"]
    
    baci.hs_id = baci.hs_id.map(lambda x: str(x).zfill(6)[:-2])
    baci.export_val = baci.export_val*1000
    
    baci = baci.set_index(["origin_id", "destination_id", 'hs_id'])
    
    baci = baci.groupby(level=['origin_id','destination_id','hs_id']).sum()
    
    baci_exports = baci.copy()
    
    baci_imports = baci.copy()
    baci_imports.columns = ["import_val"]
    baci_imports = baci_imports.swaplevel("origin_id", "destination_id")
    baci_imports = baci_imports.reset_index()
    baci_imports.columns = ["origin_id", "destination_id", "hs_id", "import_val"]
    baci_imports = baci_imports.set_index(["origin_id", "destination_id", "hs_id"])
    
    baci = baci_exports.join(baci_imports, how="outer")
    baci = baci.reset_index()
    
    country_lookup = get_country_lookup()
    hs_lookup = get_hs_lookup()
    
    baci.origin_id = baci.origin_id.astype(str)
    baci.destination_id = baci.destination_id.astype(str)
    baci["origin_id"].replace(country_lookup, inplace=True)
    baci["destination_id"].replace(country_lookup, inplace=True)
    baci["hs_id"].replace(hs_lookup, inplace=True)
    
    # need to aggregate on duplicate indexes
    baci = baci.set_index(["origin_id", "destination_id", "hs_id"])
    yodp = baci
    
    yod = yodp.groupby(level=['origin_id','destination_id']).sum()
    
    yop = yodp.groupby(level=['origin_id','hs_id']).sum()
    yop = calc_rca(yop)
    
    ydp = yodp.groupby(level=['destination_id','hs_id']).sum()
    
    yo = yodp.groupby(level=['origin_id']).sum()
    yd = yodp.groupby(level=['destination_id']).sum()
    yp = yodp.groupby(level=['hs_id']).sum()
    
    
    baci_dir = os.path.abspath(os.path.join(DATA_DIR, 'baci'))
    if not os.path.exists(baci_dir): os.makedirs(baci_dir)
    new_dir = os.path.abspath(os.path.join(DATA_DIR, 'baci', year))
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