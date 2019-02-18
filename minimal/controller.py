from nanohttp import text, Controller
from restfulpy.controllers import RootController

import minimal


class VersionController(Controller):

    @text
    def get(self):
        return minimal.application.__version__


class Root(RootController):

    version = VersionController()
