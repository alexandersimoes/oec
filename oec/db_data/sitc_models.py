from oec.db_data.abstract_models import BaseProd
from oec.db_data.abstract_models import OriginId, DestId, SitcId
from oec.db_data.abstract_models import SitcTopTrade, TopTrader, Rca, Pci

class Yd(BaseProd, DestId):
    __tablename__ = 'sitc_yd'

class Yo(BaseProd, OriginId, SitcTopTrade):
    __tablename__ = 'sitc_yo'

class Yp(BaseProd, SitcId, TopTrader, Pci):
    __tablename__ = 'sitc_yp'


class Ydp(BaseProd, DestId, SitcId):
    __tablename__ = 'sitc_ydp'

class Yod(BaseProd, OriginId, DestId):
    __tablename__ = 'sitc_yod'

class Yop(BaseProd, OriginId, SitcId, Rca):
    __tablename__ = 'sitc_yop'


class Yodp(BaseProd, OriginId, DestId, SitcId):
    __tablename__ = 'sitc_yodp'
