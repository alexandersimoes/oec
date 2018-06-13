import pandas as pd
import os, sys, bz2, gzip, zipfile, rarfile, MySQLdb
from cStringIO import StringIO

''' Are env vars set? '''


''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=os.environ.get('OEC_DB_USER'),
                        passwd=os.environ.get('OEC_DB_PW'),
                        db=os.environ.get('OEC_DB_NAME'))
db.autocommit(1)
cursor = db.cursor()

'''
    Columns:
    0 - Period
    1 - Trade Flow
    2 - Reporter
    3 - Partner
    4 - Commodity Code
    5 - Commodity Description
    6 - Trade Value
    7 - NetWeight (kg)
    8 - Unit
    9 - Trade Quantity
'''

def get_file(full_path):
    file_name = os.path.basename(full_path)
    file_path_no_ext, file_ext = os.path.splitext(file_name)

    extensions = {
        '.bz2': bz2.BZ2File,
        '.gz': gzip.open,
        '.zip': zipfile.ZipFile,
        '.rar': rarfile.RarFile
    }

    try:
        file = extensions[file_ext](full_path)
    except KeyError:
        file = open(full_path)
    except IOError:
        return None

    if file_ext == '.zip':
        file = zipfile.ZipFile.open(file, file_path_no_ext)
    elif file_ext == '.rar':
        file = rarfile.RarFile.open(file, file_path_no_ext+".csv")

    # print "Reading from file", file_name
    return file

def import_file(file_path):

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

    ''' Need to multiply by $1000 for nominal val'''
    def val_converter(val):
        return float(val)*1000

    raw_file = get_file(file_path)

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
    exports.columns = ['origin_id', 'dest_id', 'sitc_id', 'export_val']
    exports = exports.set_index(['origin_id', 'dest_id', 'sitc_id'])

    imports = imports[['Reporter', 'Partner', 'Commodity Code', 'Trade Value']]
    imports.columns = ['origin_id', 'dest_id', 'sitc_id', 'import_val']
    imports = imports.set_index(['origin_id', 'dest_id', 'sitc_id'])

    yodp = exports.join(imports, how='outer')

    yodp = yodp.reset_index(level=['origin_id', 'dest_id', 'sitc_id'])

    country_lookup = get_country_lookup()
    sitc_lookup = get_sitc_lookup()

    yodp["origin_id"].replace(country_lookup, inplace=True)
    yodp["dest_id"].replace(country_lookup, inplace=True)
    yodp["sitc_id"].replace(sitc_lookup, inplace=True)

    # need to aggregate on duplicate indexes
    yodp.groupby(yodp.index).sum()

    yodp = yodp.set_index(['origin_id', 'dest_id', 'sitc_id'])

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

    return yodp
