# -*- coding: utf-8 -*-
'''
Based on a file with the following:
country, year, total_exports, eci, neci, Fc, pci_cm, npci_cm, Qp_cm
ago, 1995, 2808927549.629999, NaN, NaN, NaN, NaN, NaN, NaN
ago, 1996, 3528848024.560000, NaN, NaN, NaN, NaN, NaN, NaN
ago, 1997, 3155605842.060000, -1.238105, -1.099466, -1.830921, 74.911660, 78.092224, 91.318694
ago, 1998, 2538135636.500002, -0.825132, -1.030300, -1.841959, 82.326454, 85.757900, 99.017278
ago, 1999, 3300421408.189999, -0.533036, -0.913696, -1.834405, 86.174819, 90.550277, 104.728454
ago, 2000, 6167065889.379999, -1.458964, -1.017590, -1.827737, 49.299154, 51.945704, 59.858853
ago, 2001, 4940329586.979995, -1.192415, -1.046041, -1.829181, 52.458849, 55.864030, 64.869426
ago, 2002, 5903271023.619997, -1.128747, -0.891448, -1.831285, 54.876672, 57.327882, 67.144364
ago, 2003, 7205875288.790001, -1.593643, -0.669955, -1.841795, 58.310621, 61.283187, 72.584441
'''
import csv, json, os, MySQLdb, sys, math

# db = MySQLdb.connect(host=os.environ.get("OEC_DB_HOST", "localhost"),
#                      user=os.environ.get("OEC_DB_USER", "root"),
#                      passwd=os.environ.get("OEC_DB_PW", ""),
#                      db=os.environ.get("OEC_DB_NAME", "oec"))
db = MySQLdb.connect(host="localhost", user="root", db="oec")
db.autocommit(1)
cursor = db.cursor()

def udpate_eci(csv_file):
    # cursor.execute("SELECT id, id_num FROM attr_country WHERE id_num IS NOT NULL;")
    # res = cursor.fetchone()

    with open(csv_file, 'r+') as eci_file:
        eci_reader = csv.reader(eci_file, delimiter=',')
        eci_reader.next()
        for line in eci_reader:
            [country, year, total_exports, eci, neci] = line[:5]
            neci = float(neci)
            year = int(year)
            if not math.isnan(neci):
                # print line
                try:
                    cursor.execute("UPDATE attr_yo SET eci=%s WHERE year=%s and SUBSTRING(origin_id, 3)=%s;", [neci, year, country])
                except MySQLdb.Error, e:
                    print "ERROR: Error in with year:{} and country:{} combination".format(year, country)
                # sys.exit()

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        sys.exit("ERROR: Need file path as argument.")
    udpate_eci(args[0])
