import pandas as pd
import os, sys, bz2, gzip, zipfile, rarfile
from __init__ import country_lookup

'''
    Columns:
    v - value in thousands of US dollars
    q - quantity in tons 
    i - exporter
    j - importer
    k - hs6
    t - year
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

def import_file(file_path, hs_id_col):
    
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
        return "{}{}".format("xx", hs6)
    
    ''' Need to multiply by $1000 for nominal val'''
    def val_converter(val):
        return float(val)*1000
    
    def country_converter(c):
        try:
            return country_lookup[int(c)]
        except:
            raise Exception("Can't find country with ID: {}".format(c))
    
    f = get_file(file_path)
    
    '''Open CSV file'''
    baci_df = pd.read_csv(f, \
                            sep=',', \
                            converters={
                                "hs6":hs6_converter, 
                                "v":val_converter, 
                                "i":country_converter, 
                                "j":country_converter})
    baci_df = baci_df[["hs6", "i", "j", "v"]]
    baci_df.columns = [hs_id_col, "origin_id", "dest_id", "export_val"]
    
    return baci_df