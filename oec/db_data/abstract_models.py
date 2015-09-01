from oec import db
from oec.utils import AutoSerialize
from oec.db_attr.models import Country, Sitc, Hs92, Hs96, Hs02, Hs07
from sqlalchemy.ext.declarative import declared_attr

class BaseProd(db.Model, AutoSerialize):
    __abstract__ = True
    year = db.Column(db.Integer(), primary_key=True)

    import_val = db.Column(db.Numeric(16,2))
    export_val = db.Column(db.Numeric(16,2))

    export_val_growth_pct = db.Column(db.Float())
    export_val_growth_pct_5 = db.Column(db.Float())
    export_val_growth_val = db.Column(db.Numeric(16,2))
    export_val_growth_val_5 = db.Column(db.Numeric(16,2))
    import_val_growth_pct = db.Column(db.Float())
    import_val_growth_pct_5 = db.Column(db.Float())
    import_val_growth_val = db.Column(db.Numeric(16,2))
    import_val_growth_val_5 = db.Column(db.Numeric(16,2))

class OriginId(object):
    @declared_attr
    def origin_id(cls):
        return db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)

class DestId(object):
    @declared_attr
    def dest_id(cls):
        return db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)

'''
    PRODUCTS
'''
class Hs92Id(object):
    hs92_id_len = db.Column(db.Integer())
    @declared_attr
    def hs92_id(cls):
        return db.Column(db.String(8), db.ForeignKey(Hs92.id), primary_key=True)

class Hs96Id(object):
    hs96_id_len = db.Column(db.Integer())
    @declared_attr
    def hs96_id(cls):
        return db.Column(db.String(8), db.ForeignKey(Hs96.id), primary_key=True)

class Hs02Id(object):
    hs02_id_len = db.Column(db.Integer())
    @declared_attr
    def hs02_id(cls):
        return db.Column(db.String(8), db.ForeignKey(Hs02.id), primary_key=True)

class Hs07Id(object):
    hs07_id_len = db.Column(db.Integer())
    @declared_attr
    def hs07_id(cls):
        return db.Column(db.String(8), db.ForeignKey(Hs07.id), primary_key=True)

class SitcId(object):
    sitc_id_len = db.Column(db.Integer())
    @declared_attr
    def sitc_id(cls):
        return db.Column(db.String(8), db.ForeignKey(Sitc.id), primary_key=True)

class SitcTopTrade(object):
    top_export_dest = db.Column(db.String(5))
    top_import_dest = db.Column(db.String(5))
    
    @declared_attr
    def top_export(cls):
        return db.Column(db.String(6), db.ForeignKey(Sitc.id))
    
    @declared_attr
    def top_import(cls):
        return db.Column(db.String(6), db.ForeignKey(Sitc.id))

class HsTopTrade(object):
    top_export_dest = db.Column(db.String(5))
    top_import_dest = db.Column(db.String(5))
    
    @declared_attr
    def top_export_hs4(cls):
        return db.Column(db.String(6), db.ForeignKey(Hs92.id))
    @declared_attr
    def top_export_hs6(cls):
        return db.Column(db.String(8), db.ForeignKey(Hs92.id))
    
    @declared_attr
    def top_import_hs4(cls):
        return db.Column(db.String(6), db.ForeignKey(Hs92.id))
    @declared_attr
    def top_import_hs6(cls):
        return db.Column(db.String(8), db.ForeignKey(Hs92.id))

class TopTrader(object):
    
    @declared_attr
    def top_exporter(cls):
        return db.Column(db.String(5), db.ForeignKey(Country.id))
    
    @declared_attr
    def top_importer(cls):
        return db.Column(db.String(5), db.ForeignKey(Country.id))

class Rca(object):
    export_rca = db.Column(db.Float())
    import_rca = db.Column(db.Float())

class Pci(object):
    pci = db.Column(db.Float())
    pci_rank = db.Column(db.Integer)
    pci_rank_delta = db.Column(db.Integer)
