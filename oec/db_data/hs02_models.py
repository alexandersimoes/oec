from oec.db_data.abstract_models import BaseProd
from oec.db_data.abstract_models import OriginId, DestId, Hs02Id
from oec.db_data.abstract_models import HsTopTrade, TopTrader, Rca, Pci

class Yd(BaseProd, DestId):
    __tablename__ = 'hs02_yd'

class Yo(BaseProd, OriginId, HsTopTrade):
    __tablename__ = 'hs02_yo'

class Yp(BaseProd, Hs02Id, TopTrader, Pci):
    __tablename__ = 'hs02_yp'


class Ydp(BaseProd, DestId, Hs02Id):
    __tablename__ = 'hs02_ydp'

class Yod(BaseProd, OriginId, DestId):
    __tablename__ = 'hs02_yod'

class Yop(BaseProd, OriginId, Hs02Id, Rca):
    __tablename__ = 'hs02_yop'


class Yodp(BaseProd, OriginId, DestId, Hs02Id):
    __tablename__ = 'hs02_yodp'
