import urllib, json, MySQLdb, os
import pandas as pd

''' Connect to DB '''
db = MySQLdb.connect(host="localhost", user=os.environ["OEC_DB_USER"],
                        passwd=os.environ["OEC_DB_PW"], 
                        db=os.environ["OEC_DB_NAME"])
db.autocommit(1)
cursor = db.cursor()

def get_attr_yo(year):
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