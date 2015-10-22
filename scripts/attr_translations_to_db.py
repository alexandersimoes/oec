# -*- coding: utf-8 -*-
"""
    Add HS/SITC product translations to DB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Raw data from this file - 
    https://docs.google.com/spreadsheets/d/1mPG5zgQmeh3vRsGQrIOq8hPONXNRGW1OC449ExAqMVs/

"""
import sys, MySQLdb, time, os, csv, argparse, click

''' Connect to DB '''
db = MySQLdb.connect(host=os.environ.get("OEC_DB_HOST"), user=os.environ.get("OEC_DB_USER"), 
                        passwd=os.environ.get("OEC_DB_PW"), 
                        db=os.environ.get("OEC_DB_NAME"))
db.autocommit(1)
cursor = db.cursor()

oec_langs = ['ar','de','el','en','es','fr','he','hi','it','ja','ko','mn','nl','ru','pt','tr','vi','zh_cn']

@click.command()
@click.argument('file_path', type=click.File('rb'))
@click.option('-l', '--lang', prompt='Language', help='2 letter lang code of translations', required=True, type=click.Choice(oec_langs))
@click.option('-c', '--cls', prompt='Classification', required=True, type=click.Choice(['hs', 'hs92', 'hs96', 'hs02', 'hs07', 'sitc', 'country']))
def main(file_path, lang, cls):
    
    '''Initialize lookup for column indicies'''
    col_positions = {
        "id": None,
        "name": None
    }
    if cls in ['hs', 'sitc', 'hs92', 'hs96', 'hs02', 'hs07']:
        col_positions["desc"] = None
        col_positions["keywords"] = None
        col_positions["article"] = None
        col_positions["plural"] = None
        col_positions["gender"] = None
    
    with file_path as csv_file:
        
        '''if the lang is not english skip the first line (these are the instructions)'''
        if lang != "en": next(csv_file)
        
        csv_reader = csv.reader(csv_file, delimiter='\t', quotechar='"')
        for row, data in enumerate(csv_reader):
            
            '''if its the first row setup col_positions'''
            if row == 0:
                
                
                print; print "First row index and column names for reference: "
                for column, column_header in enumerate(data):
                    print column, column_header
                print
                
                '''step thru each column to set indicies'''
                for col_name in col_positions:
                    try:
                        col_positions[col_name] = int(raw_input("Index for " + col_name + " column: "))
                    except:
                        print "Must be integer..."; sys.exit()
                
                print "Adding names to DB..."
                continue
            
            '''make a copy of col_positions so we dont overwrite original'''
            vals = col_positions.copy()
            
            '''fill in vals with data from CSV'''
            for col_name in vals:
                vals[col_name] = data[col_positions[col_name]] or None
                vals[col_name] = None if vals[col_name] == "#VALUE!" else vals[col_name]
                if col_name == "keywords" and vals[col_name]:
                    vals[col_name] = [x.strip() for x in vals[col_name].replace("و", ",").replace("，", ",").replace("、", ",").split(",")]
                    vals[col_name] = ", ".join(vals[col_name])
                        
            if vals["name"]:
                
                if cls in ['hs', 'sitc', 'hs92', 'hs96', 'hs02', 'hs07']:
                    indicies = [vals["id"], lang]
                    data_vals = [vals["name"], vals["keywords"], vals["desc"], vals["gender"], vals["plural"], vals["article"]]
                
                    sql = """
                    INSERT INTO attr_{0}_name
                      ({0}_id, lang, name, keywords, `desc`, gender, plural, article)
                    VALUES
                      (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                      name=%s, keywords=%s, `desc`=%s, gender=%s, plural=%s, article=%s
                    """.format(cls)
                
                else:
                    indicies = [vals["id"], lang]
                    data_vals = [vals["name"]]
                
                    sql = """
                    INSERT INTO attr_{0}_name
                      (origin_id, lang, name)
                    VALUES
                      (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                      name=%s
                    """.format(cls)
                    
                # print sql
                # sys.exit()
            
                try:
                    cursor.execute(sql, indicies+data_vals+data_vals)
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    print indicies
                    # sys.exit()
                    

if __name__ == "__main__":
    main()
