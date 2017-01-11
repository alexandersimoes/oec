# -*- coding: utf-8 -*-
import os, sys, MySQLdb, csv

''' Connect to DB '''
db = MySQLdb.connect(host=os.environ.get("OEC_DB_HOST"), user=os.environ.get("OEC_DB_UN"),
                        passwd=os.environ.get("OEC_DB_PW"), db=os.environ.get("OEC_DB_DB"))
cursor = db.cursor()

file_path = "products.csv"
with open(file_path) as f:
  f.seek(0)
  csv_data = csv.reader(f, delimiter=",")
  headers = csv_data.next()
  for i, row in enumerate(csv_data):

    sitc_id, id, y, x, pini, sitc_name, pini_class = row

    if pini:
      pini = float(pini)

      cursor.execute("""
        UPDATE attr_sitc set pini=%s, pini_class=%s
        WHERE id=%s
      """, [pini, pini_class, id])

    #close the connection to the database.
    db.commit()
