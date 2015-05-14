import os, sys
from calc_rca import calc_rca

file_path = os.path.dirname(os.path.realpath(__file__))
ps_calcs_lib_path = os.path.abspath(os.path.join(file_path, "../../../lib/ps_calcs"))
sys.path.insert(0, ps_calcs_lib_path)
import ps_calcs

def calc_complexity(attr_yo, yp, yop, year):
    ubiquity_required = 20
    diversity_required = 200
    total_exports_required = 50000000
    population_required = 1000000
    
    '''trim country list by diversity'''
    origin_diversity = yop.reset_index()
    origin_diversity = origin_diversity["origin_id"].value_counts()
    origin_diversity = origin_diversity[origin_diversity > diversity_required]
    
    '''trim country list by total exports'''
    origin_totals = yop.groupby(level=['origin_id']).sum()
    origin_totals = origin_totals['export_val']
    origin_totals = origin_totals[origin_totals > total_exports_required]
    
    '''trim country list by population'''
    origin_pop = attr_yo[attr_yo["population"] > population_required]
    
    filtered_origins = set(origin_diversity.index).intersection(set(origin_totals.index)).intersection(set(origin_pop.index))
    
    '''trim product list by ubiquity'''
    product_ubiquity = yop.reset_index()
    product_ubiquity = product_ubiquity["hs_id"].value_counts()
    product_ubiquity = product_ubiquity[product_ubiquity > ubiquity_required]
    
    filtered_products = set(product_ubiquity.index)
    
    '''re-calculate rcas'''
    yop_rcas = yop[["export_val", "import_val"]]
    origins_to_drop = set(yop_rcas.index.get_level_values('origin_id')).difference(filtered_origins)
    products_to_drop = set(yop_rcas.index.get_level_values('hs_id')).difference(filtered_products)
    yop_rcas = yop_rcas.drop(list(origins_to_drop), axis=0, level='origin_id')
    yop_rcas = yop_rcas.drop(list(products_to_drop), axis=0, level='hs_id')
    yop_rcas = calc_rca(yop_rcas)
    
    '''pivot RCAs'''
    yop_rcas = yop_rcas[["export_rca"]].dropna()
    yop_rcas = yop_rcas.reset_index()
    yop_rcas = yop_rcas.pivot(index="origin_id", columns="hs_id", values="export_rca")
    
    '''change RCAs to binary'''
    yop_rcas[yop_rcas >= 1] = 1
    yop_rcas[yop_rcas < 1] = 0
    
    '''for testing'''
    # eci, pci = complexity(yop_rcas.fillna(0))
    # q = "select id as {0}_id, name from attr_{0}, attr_{0}_name where {0}_id = id and lang = 'en' and length(id) = 6".format(classification)
    # p_names = sql.read_frame(q, db, index_col=p_id)
    # p_names["pci"] = pci
    # p_names["pci_rank"] = pci.rank(ascending=False)
    # print p_names.sort(['pci_rank']).head(20)
    
    '''calculate complexity'''
    eci, pci = ps_calcs.complexity(yop_rcas.fillna(0))
    
    yp["pci"] = pci
    yp["pci_rank"] = pci.rank(ascending=False)
    
    attr_yo["eci"] = eci
    attr_yo["eci_rank"] = eci.rank(ascending=False)
    
    # '''get previous years values'''
    # q = "select hs_id, pci_rank from hs_yp where year = {0}".format(int(year)-1)
    # prev_year_pci = sql.read_frame(q, db, index_col="hs_id")
    # yp["pci_rank_delta"] = prev_year_pci["pci_rank"] - yp["pci_rank"]
    #
    # q = "select origin_id, eci_rank from attr_yo where year = {0}".format(int(year)-1)
    # prev_year_eci = sql.read_frame(q, db, index_col="origin_id")
    # attr_yo["eci_rank_delta"] = prev_year_eci["eci_rank"] - attr_yo["eci_rank"]
    
    return attr_yo, yp
