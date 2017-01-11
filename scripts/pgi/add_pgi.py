# -*- coding: utf-8 -*-
import os, sys, MySQLdb, csv

''' Connect to DB '''
db = MySQLdb.connect(host=os.environ.get("OEC_DB_HOST"), user=os.environ.get("OEC_DB_UN"),
                        passwd=os.environ.get("OEC_DB_PW"), db=os.environ.get("OEC_DB_DB"))
cursor = db.cursor()

file_path = "indicators.csv"
with open(file_path) as f:
  f.seek(0)
  csv_data = csv.reader(f, delimiter=",")
  headers = csv_data.next()
  for i, row in enumerate(csv_data):

    year, cid, eci, gini, xgini, gdppc = row
    year = float(year)

    if xgini:
      xgini = float(xgini)

      cursor.execute("""
        UPDATE attr_yo set xgini=%s
        WHERE year=%s and substr(origin_id, 3)=%s
      """, [xgini, year, cid])

    if gini:
      gini = float(gini)

      cursor.execute("""
        UPDATE attr_yo set gini=%s
        WHERE year=%s and substr(origin_id, 3)=%s
      """, [gini, year, cid])

    #close the connection to the database.
    db.commit()
