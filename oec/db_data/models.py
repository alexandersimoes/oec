from oec.db_hs.abstract_models import BaseHs
from oec.db_hs.abstract_models import OriginId, DestId, Hs92Id
from oec.db_hs.abstract_models import TopTrade, TopTrader, Rca, Pci

class Yd(BaseHs, DestId):
    __tablename__ = 'hs92_yd'

class Yo(BaseHs, OriginId, TopTrade):
    __tablename__ = 'hs92_yo'

class Yp(BaseHs, Hs92Id, TopTrader, Pci):
    __tablename__ = 'hs92_yp'


class Ydp(BaseHs, DestId, Hs92Id):
    __tablename__ = 'hs92_ydp'

class Yod(BaseHs, OriginId, DestId):
    __tablename__ = 'hs92_yod'

class Yop(BaseHs, OriginId, Hs92Id, Rca):
    __tablename__ = 'hs92_yop'


class Yodp(BaseHs, OriginId, DestId, Hs92Id):
    __tablename__ = 'hs_yodp'
