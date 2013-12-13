from oec import db
from oec.utils import AutoSerialize
from oec.db_attr.models import Country, Sitc

class Yo(db.Model, AutoSerialize):
    
    __tablename__ = 'sitc_yo'
    
    year = db.Column(db.Integer(4), primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Yo %d.%s>' % (self.year, self.origin_id)

class Yd(db.Model, AutoSerialize):
    
    __tablename__ = 'sitc_yd'
    
    year = db.Column(db.Integer(4), primary_key=True)
    dest_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Yd %d.%s>' % (self.year, self.dest_id)

class Yp(db.Model, AutoSerialize):
    
    __tablename__ = 'sitc_yp'
    
    year = db.Column(db.Integer(4), primary_key=True)
    sitc_id = db.Column(db.String(8), db.ForeignKey(Sitc.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Yp %d.%s>' % (self.year, self.sitc_id)

class Yop(db.Model, AutoSerialize):
    
    __tablename__ = 'sitc_yop'
    
    year = db.Column(db.Integer(4), primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    sitc_id = db.Column(db.String(8), db.ForeignKey(Sitc.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    export_rca = db.Column(db.Float())
    import_rca = db.Column(db.Float())
    
    def __repr__(self):
        return '<Yop %d.%s.%s>' % (self.year, self.origin_id, self.sitc_id)

class Yod(db.Model, AutoSerialize):
    
    __tablename__ = 'sitc_yod'
    
    year = db.Column(db.Integer(4), primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    dest_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Yod %d.%s.%s>' % (self.year, self.origin_id, self.dest_id)

class Ydp(db.Model, AutoSerialize):
    
    __tablename__ = 'sitc_ydp'
    
    year = db.Column(db.Integer(4), primary_key=True)
    dest_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    sitc_id = db.Column(db.String(8), db.ForeignKey(Sitc.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Ydp %d.%s.%s>' % (self.year, self.dest_id, self.sitc_id)

class Yodp(db.Model, AutoSerialize):
    
    __tablename__ = 'sitc_yodp'
    
    year = db.Column(db.Integer(4), primary_key=True)
    origin_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    dest_id = db.Column(db.String(5), db.ForeignKey(Country.id), primary_key=True)
    sitc_id = db.Column(db.String(8), db.ForeignKey(Sitc.id), primary_key=True)
    export_val = db.Column(db.Numeric(16,2))
    import_val = db.Column(db.Numeric(16,2))
    
    def __repr__(self):
        return '<Yodp %d.%s.%s.%s>' % (self.year, self.origin_id, self.dest_id, self.sitc_id)