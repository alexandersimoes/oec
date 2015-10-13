import json, os, MySQLdb

db = MySQLdb.connect(host=os.environ.get("OEC_DB_HOST", "localhost"),
                     user=os.environ.get("OEC_DB_USER", "root"),
                     passwd=os.environ.get("OEC_DB_PW", ""),
                     db=os.environ.get("OEC_DB_NAME", "oec"))
db.autocommit(1)
cursor = db.cursor()

def read_json():

    cursor.execute("SELECT id, id_num FROM attr_country WHERE id_num IS NOT NULL;")
    res = cursor.fetchall()
    lookup = {}
    for a in res:
        if "|" in a[1]:
            ids = a[1].split("|")
            for i in ids:
                lookup[i] = a[0]
        else:
            lookup[a[1]] = a[0]

    with open('oec/static/json/country_coords.json', 'r+') as data_file:
        data = json.load(data_file)
        for geo in data["objects"]["countries"]["geometries"]:
            geo["id"] = str(geo["id"])
            if geo["id"] in lookup:
                geo["id"] = lookup[geo["id"]]
        data_file.seek(0)
        json.dump(data, data_file)

if __name__ == '__main__':
    read_json()
