from oec import db
from oec.utils import AutoSerialize
from oec.db_attr.models import Country, Hs
# from sqlalchemy import op

class Yo(db.Model, AutoSerialize):
    
    __tablename__ = 'hs_yo'
    
    year = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    top_export = db.Column(db.String(8), db.ForeignKey(Hs.id))
    
    def __repr__(self):
        return '<Yo %d.%s>' % (self.year, self.origin_id)

class Yd(db.Model, AutoSerialize):
    
    __tablename__ = 'hs_yd'
    
    year = db.Column(db.Integer, primary_key=True)
    dest_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Yd %d.%s>' % (self.year, self.dest_id)

class Yp(db.Model, AutoSerialize):
    
    __tablename__ = 'hs_yp'
    
    year = db.Column(db.Integer, primary_key=True)
    hs_id = db.Column(db.String(8), db.ForeignKey(Hs.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    pci = db.Column(db.Float())
    pci_rank = db.Column(db.Integer)
    top_exporter = db.Column(db.String(5), db.ForeignKey(Country.id))
    
    def __repr__(self):
        return '<Yp %d.%s>' % (self.year, self.hs_id)

class Yop(db.Model, AutoSerialize):
    
    __tablename__ = 'hs_yop'
    
    year = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    hs_id = db.Column(db.String(8), db.ForeignKey(Hs.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    export_rca = db.Column(db.Float())
    import_rca = db.Column(db.Float())
    
    export_val_growth_pct = db.Column(db.Float())
    export_val_growth_pct_5 = db.Column(db.Float())
    export_val_growth_val = db.Column(db.Numeric(16,2))
    export_val_growth_val_5 = db.Column(db.Numeric(16,2))
    import_val_growth_pct = db.Column(db.Float())
    import_val_growth_pct_5 = db.Column(db.Float())
    import_val_growth_val = db.Column(db.Numeric(16,2))
    import_val_growth_val_5 = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Yop %d.%s.%s>' % (self.year, self.origin_id, self.hs_id)

class Yod(db.Model, AutoSerialize):
    
    __tablename__ = 'hs_yod'
    
    year = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    dest_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Yod %d.%s.%s>' % (self.year, self.origin_id, self.dest_id)

class Ydp(db.Model, AutoSerialize):
    
    __tablename__ = 'hs_ydp'
    
    year = db.Column(db.Integer, primary_key=True)
    dest_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    hs_id = db.Column(db.String(8), db.ForeignKey(Hs.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Ydp %d.%s.%s>' % (self.year, self.dest_id, self.hs_id)

class Yodp(db.Model, AutoSerialize):
    
    __tablename__ = 'hs_yodp'
    
    year = db.Column(db.Integer, primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    dest_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    hs_id = db.Column(db.String(8), db.ForeignKey(Hs.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Yodp %d.%s.%s.%s>' % (self.year, self.origin_id, self.dest_id, self.hs_id)