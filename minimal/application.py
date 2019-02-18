from os.path import join, dirname

from minimal.cell import Cell
from minimal.cli import Start
from restfulpy.application import Application
from restfulpy.orm import DBSession

from .controller import Root


__version__ = '0.1.0'


class Minimal(Application):

    __configuration__ = '''
        debug: True

        db:
          echo: False
          url: postgresql://postgres:postgres@localhost/minimal_dev
          test_url: postgresql://postgres:postgres@localhost/minimal_test
          administrative_url: postgresql://postgres:postgres@localhost/postgres

    '''

    def __init__(self):
        super().__init__(
            'owl',
            root=Root(),
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    def register_cli_launchers(self, subparsers):
        Start(subparsers=subparsers)

    def insert_basedata(self):  # pragma: no cover
        cell1 = Cell(x=0, y=0, is_alive=True)
        DBSession.add(cell1)
        cell2 = Cell(x=1, y=0, is_alive=True)
        DBSession.add(cell2)
        cell3 = Cell(x=0, y=1, is_alive=True)
        DBSession.add(cell3)
        cell4 = Cell(x=1, y=1)
        DBSession.add(cell4)

        DBSession.commit()

    def insert_mockup(self, *args):  # pragma: no cover
        pass
