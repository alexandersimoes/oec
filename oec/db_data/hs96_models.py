from oec.db_data.abstract_models import BaseProd
from oec.db_data.abstract_models import OriginId, DestId, Hs96Id
from oec.db_data.abstract_models import HsTopTrade, TopTrader, Rca, Pci

class Yd(BaseProd, DestId):
    __tablename__ = 'hs96_yd'

class Yo(BaseProd, OriginId, HsTopTrade):
    __tablename__ = 'hs96_yo'

class Yp(BaseProd, Hs96Id, TopTrader, Pci):
    __tablename__ = 'hs96_yp'


class Ydp(BaseProd, DestId, Hs96Id):
    __tablename__ = 'hs96_ydp'

class Yod(BaseProd, OriginId, DestId):
    __tablename__ = 'hs96_yod'

class Yop(BaseProd, OriginId, Hs96Id, Rca):
    __tablename__ = 'hs96_yop'


class Yodp(BaseProd, OriginId, DestId, Hs96Id):
    __tablename__ = 'hs96_yodp'
