from oec.db_data.abstract_models import BaseProd
from oec.db_data.abstract_models import OriginId, DestId, Hs07Id
from oec.db_data.abstract_models import HsTopTrade, TopTrader, Rca, Pci

class Yd(BaseProd, DestId):
    __tablename__ = 'hs07_yd'

class Yo(BaseProd, OriginId, HsTopTrade):
    __tablename__ = 'hs07_yo'

class Yp(BaseProd, Hs07Id, TopTrader, Pci):
    __tablename__ = 'hs07_yp'


class Ydp(BaseProd, DestId, Hs07Id):
    __tablename__ = 'hs07_ydp'

class Yod(BaseProd, OriginId, DestId):
    __tablename__ = 'hs07_yod'

class Yop(BaseProd, OriginId, Hs07Id, Rca):
    __tablename__ = 'hs07_yop'


class Yodp(BaseProd, OriginId, DestId, Hs07Id):
    __tablename__ = 'hs07_yodp'
