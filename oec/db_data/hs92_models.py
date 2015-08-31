from oec.db_data.abstract_models import BaseProd
from oec.db_data.abstract_models import OriginId, DestId, Hs92Id
from oec.db_data.abstract_models import HsTopTrade, TopTrader, Rca, Pci

class Yd(BaseProd, DestId):
    __tablename__ = 'hs92_yd'

class Yo(BaseProd, OriginId, HsTopTrade):
    __tablename__ = 'hs92_yo'

class Yp(BaseProd, Hs92Id, TopTrader, Pci):
    __tablename__ = 'hs92_yp'


class Ydp(BaseProd, DestId, Hs92Id):
    __tablename__ = 'hs92_ydp'

class Yod(BaseProd, OriginId, DestId):
    __tablename__ = 'hs92_yod'

class Yop(BaseProd, OriginId, Hs92Id, Rca):
    __tablename__ = 'hs92_yop'


class Yodp(BaseProd, OriginId, DestId, Hs92Id):
    __tablename__ = 'hs92_yodp'
