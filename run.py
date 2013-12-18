from flask.ext.script import Manager
from oec import app

manager = Manager(app)
manager.run()
