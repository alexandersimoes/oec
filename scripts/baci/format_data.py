# -*- coding: utf-8 -*-
"""
    Format BACI data for DB entry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Columns:
    v - value in thousands of US dollars
    q - quantity in tons 
    i - exporter
    j - importer
    k - hs6
    t - year
    
    Example Usage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    python -m scripts.baci.format_data /Users/alexandersimoes/Downloads/baci92_2012.csv -y 2012

"""

''' Import statements '''
import os, sys, time, MySQLdb, bz2, click, urllib, json
import pandas as pd
import pandas.io.sql as sql
import numpy as np
from helpers import country_lookup
from helpers.calc_rca import calc_rca
from helpers.calc_top_prod_dest import calc_top_prod_dest
from helpers.calc_complexity import calc_complexity

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=os.environ["OEC_DB_USER"],
                        passwd=os.environ["OEC_DB_PW"], 
                        db=os.environ["OEC_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def import_file(file_path):
    
    def hs6_converter(hs6):
        leading2 = int(hs6[:2])
        if leading2 <= 5: return "{}{}".format("01", hs6)
        if leading2 <= 14: return "{}{}".format("02", hs6)
        if leading2 <= 15: return "{}{}".format("03", hs6)
        if leading2 <= 24: return "{}{}".format("04", hs6)
        if leading2 <= 27: return "{}{}".format("05", hs6)
        if leading2 <= 38: return "{}{}".format("06", hs6)
        if leading2 <= 40: return "{}{}".format("07", hs6)
        if leading2 <= 43: return "{}{}".format("08", hs6)
        if leading2 <= 46: return "{}{}".format("09", hs6)
        if leading2 <= 49: return "{}{}".format("10", hs6)
        if leading2 <= 63: return "{}{}".format("11", hs6)
        if leading2 <= 67: return "{}{}".format("12", hs6)
        if leading2 <= 70: return "{}{}".format("13", hs6)
        if leading2 <= 71: return "{}{}".format("14", hs6)
        if leading2 <= 83: return "{}{}".format("15", hs6)
        if leading2 <= 85: return "{}{}".format("16", hs6)
        if leading2 <= 89: return "{}{}".format("17", hs6)
        if leading2 <= 92: return "{}{}".format("18", hs6)
        if leading2 <= 93: return "{}{}".format("19", hs6)
        if leading2 <= 96: return "{}{}".format("20", hs6)
        if leading2 <= 97: return "{}{}".format("21", hs6)
        if leading2 <= 99: return "{}{}".format("22", hs6)
        return "{}{}".format("03", hs6)
    
    ''' Need to multiply by $1000 for nominal val'''
    def val_converter(val):
        return float(val)*1000
    
    def country_converter(c):
        try:
            return country_lookup[int(c)]
        except:
            raise Exception("Can't find country with ID: {}".format(c))
    
    '''Open CSV file'''
    baci_df = pd.read_csv(file_path, sep=',', converters={"hs6":hs6_converter, "v":val_converter, "i":country_converter, "j":country_converter})
    baci_df = baci_df[["hs6", "i", "j", "v"]]
    baci_df.columns = ["hs_id", "origin_id", "dest_id", "export_val"]
    
    return baci_df

def add_index(baci_df):
    baci_df = baci_df.set_index(["origin_id", "dest_id", "hs_id"])
    baci_df = baci_df.groupby(level=['origin_id', 'dest_id', 'hs_id']).sum()
    
    baci_df_import = baci_df.copy()
    baci_df_import.columns = ['import_val']
    baci_df_import = baci_df_import.swaplevel('origin_id', 'dest_id')
    baci_df_import.index.names = ['origin_id', 'dest_id', 'hs_id']
    
    baci_df = pd.merge(baci_df, baci_df_import, right_index=True, left_index=True, how='outer')
    
    return baci_df

def calc_growth(year, table_name, table):
    print table_name, "growth..."
    
    def get_index(table_name):
        lookup = {"o":"origin_id", "d":"dest_id", "p":"hs_id"}
        return [lookup[var] for var in table_name[1:]]
    
    index = get_index(table_name)
    cls = "hs"
    
    print '''Loading previous year'''
    q = "select * from {0}_{1} where year = {2}".format(cls, table_name, int(year)-1)
    prev_yr = sql.read_frame(q, db, index_col=index)
    
    if prev_yr.empty:
        print "No data for previous year, unable to calculate growth."
        return table
    
    print "calculating 1 year export value growth"
    table["export_val_growth_val"] = table["export_val"] - prev_yr["export_val"]
    
    print "calculating 1 year import value growth"
    table["import_val_growth_val"] = table["import_val"] - prev_yr["import_val"]
    
    print "calculating 1 year export value growth percent"
    table["export_val_growth_pct"] = (table["export_val"] / prev_yr["export_val"]) - 1
    
    print "calculating 1 year import value growth percent"
    table["import_val_growth_pct"] = (table["import_val"] / prev_yr["import_val"]) - 1
    
    print '''Loading previous 5 year values'''
    q = "select * from {0}_{1} where year = {2}".format(cls, table_name, int(year)-5)
    prev5_yr = sql.read_frame(q, db, index_col=index)
    
    if prev5_yr.empty:
        print "No data for 5 years ago, unable to calculate 5 year growth"
        return table
    
    print "calculating 1 year export value growth"
    table["export_val_growth_val_5"] = table["export_val"] - prev5_yr["export_val"]

    print "calculating 1 year import value growth"
    table["import_val_growth_val_5"] = table["import_val"] - prev5_yr["import_val"]

    print "calculating 1 year export value growth percent"
    table["export_val_growth_pct_5"] = (table["export_val"] / prev5_yr["export_val"]) ** (1.0/5.0) - 1

    print "calculating 1 year import value growth percent"
    table["import_val_growth_pct_5"] = (table["import_val"] / prev5_yr["import_val"]) ** (1.0/5.0) - 1
    
    table = table.replace(to_replace=np.inf, value=np.nan)
    table = table.replace(0, np.nan)
    # table = table.where((pd.notnull(table)), None)
    
    return table

def write_to_files(year, dfs):
    for df in dfs:
        name, data = df
        
        '''reorder columns so year is first'''
        data = data.reset_index()
        data["year"] = year
        cols = data.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        data = data[cols]
        
        '''make sure directory exists'''
        baci_dir = os.path.abspath(os.path.join(DATA_DIR, 'baci', str(year)))
        if not os.path.exists(baci_dir): os.makedirs(baci_dir)
        
        '''create new BZ2 formatted file'''
        new_file_path = os.path.abspath(os.path.join(baci_dir, "hs_"+name+".tsv.bz2"))
        print ' writing file: ', name
        data.to_csv(bz2.BZ2File(new_file_path, 'wb'), sep="\t", index=False)

def get_attr_yo(year):
    indicators = {
        "population": "SP.POP.TOTL",
        "gdp": "NY.GDP.MKTP.CD",
        "gdp_pc": "NY.GDP.PCAP.CD"
    }
    cursor.execute("select id_2char, id from attr_country where id_2char is not null;")
    id_crosswalk = {r[0].upper():r[1] for r in cursor.fetchall()}
    yo_attr = pd.DataFrame()
    
    for i_name, i_id in indicators.items():
        wdi_url = "http://api.worldbank.org/countries/all/indicators/{0}?format=json&date={1}&per_page=300".format(i_id, year)
        response = urllib.urlopen(wdi_url);
        wdi_data = json.loads(response.read())
        wdi_data = wdi_data[1]
        wdi_data = [[x["country"]["id"], x["value"]] for x in wdi_data]
        wdi_data = pd.DataFrame(wdi_data, columns=["origin_id", i_name])
        wdi_data[i_name] = wdi_data[i_name].astype(float)
        
        wdi_data["origin_id"] = wdi_data["origin_id"].replace(id_crosswalk)
        wdi_data = wdi_data.set_index("origin_id")
        wdi_data_index = [x for x in wdi_data.index if len(x)==5]
        wdi_data = wdi_data.reindex(index=wdi_data_index).dropna()
        
        if yo_attr.empty:
            yo_attr = wdi_data
        else:
            yo_attr[i_name] = wdi_data[i_name]
        
    return yo_attr

@click.command()
@click.argument('input_file', type=click.File('rb'))
@click.option('-y', '--year', prompt='Year', help='year of the data to convert', required=True, type=int)
@click.option('-o', '--output_dir', help='output directory', type=click.Path(), default="data/baci")
def main(input_file, year, output_dir):
    attr_yo = get_attr_yo(year)
    
    output_dir = os.path.abspath(os.path.join(output_dir, str(year)))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    store = pd.HDFStore(os.path.join(output_dir,'yodp.h5'))
    
    try:
        yodp = store.get('yodp')
    except KeyError:
        '''
        STEP 1:
        Import file to pandas dataframe.'''
        baci_df = import_file(input_file)
    
        '''
        STEP 2:
        Add indexes'''
        yodp = add_index(baci_df)
        
        store.put('yodp', yodp)
    
    '''
    STEP 3:
    Aggregate'''
    yod = yodp.groupby(level=['origin_id','dest_id']).sum()
    yop = yodp.groupby(level=['origin_id','hs_id']).sum()
    ydp = yodp.groupby(level=['dest_id','hs_id']).sum()
    yo = yodp.groupby(level=['origin_id']).sum()
    yd = yodp.groupby(level=['dest_id']).sum()
    yp = yodp.groupby(level=['hs_id']).sum()
    
    '''
    STEP 4:
    Calculate RCA'''
    yop = calc_rca(yop)
    
    '''
    STEP 5:
    Calculate top product and destination'''
    yo, yp = calc_top_prod_dest(yo, yp, yop, yod)
    
    '''
    STEP 6:
    Calculate complexity'''
    attr_yo, yp = calc_complexity(attr_yo, yp, yop, year)
    
    print yp.head()
    sys.exit()
    
    '''
    STEP 4:
    Growth'''
    tables = {"yodp":yodp, "yop":yop, "yod":yod, "ydp":ydp, "yo":yo, "yp":yp, "yd":yd}
    for table_name in tables:
        tables[table_name] = calc_growth(year, table_name, tables[table_name])
    
    '''
    STEP 5:
    Write out to files'''
    tables["attr_yo"] = attr_yo
    write_to_files(year, tables.items())

if __name__ == "__main__":
    start = time.time()

    main()
    
    total_run_time = (time.time() - start) / 60
    print; print;
    print "Total runtime: {0} minutes".format(int(total_run_time))
    print; print;