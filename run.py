from oec import app

from flask.ext.script import Manager
manager = Manager(app)
manager.run()
