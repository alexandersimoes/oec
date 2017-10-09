import urllib, json, MySQLdb, os, sys
import pandas as pd

''' Connect to DB '''
db = MySQLdb.connect(host=os.environ["OEC_DB_HOST"],
                        user=os.environ["OEC_DB_USER"],
                        passwd=os.environ["OEC_DB_PW"],
                        db=os.environ["OEC_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()
YEAR = 2016

def get_wdi(year):
    indicators = {
        "population": "SP.POP.TOTL",
        "gdp": "NY.GDP.MKTP.CD",
        "gdp_pc_current": "NY.GDP.PCAP.CD",
        "gdp_pc_constant": "NY.GDP.PCAP.KD",
        "gdp_pc_current_ppp": "NY.GDP.PCAP.PP.CD",
        "gdp_pc_constant_ppp": "NY.GDP.PCAP.PP.KD"
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
        if wdi_data.empty:
            print "No data found for '{}' indicator.".format(i_name)
            continue
        wdi_data[i_name] = wdi_data[i_name].astype(float)

        wdi_data["origin_id"] = wdi_data["origin_id"].replace(id_crosswalk)
        wdi_data = wdi_data.set_index("origin_id")
        wdi_data_index = [x for x in wdi_data.index if len(x)==5]
        wdi_data = wdi_data.reindex(index=wdi_data_index).dropna()

        if yo_attr.empty:
            yo_attr = wdi_data
        else:
            yo_attr[i_name] = wdi_data[i_name]

    print yo_attr.head()
    return yo_attr

def add_yo_to_db(yo_attr, year):
    for origin_id, row in yo_attr.iterrows():
        print "updating {}".format(origin_id)
        row = {k:(None if pd.isnull(v) else v) for k, v in row.to_dict().items()}
        try:
            cursor.execute("""UPDATE attr_yo
            SET gdp=%s, gdp_pc_current=%s, gdp_pc_constant=%s, gdp_pc_current_ppp=%s, gdp_pc_constant_ppp=%s, population=%s
            WHERE year=%s and origin_id=%s;
            """, [row["gdp"], row["gdp_pc_current"], row["gdp_pc_constant"], row["gdp_pc_current_ppp"], row["gdp_pc_constant_ppp"], row["population"], year, origin_id])
        except MySQLdb.Error, e:
            print "ERROR: Error in with year:{} and country:{} combination".format(year, origin_id)

if __name__ == "__main__":
    yo_attr = get_wdi(YEAR)
    add_yo_to_db(yo_attr, YEAR)
