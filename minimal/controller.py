from nanohttp import text
from restfulpy.controllers import RootController, RestController

import minimal


class VersionController(RestController):

    @text
    def get(self):
        return minimal.application.__version__

class Root(RootController):

    version = VersionController()
