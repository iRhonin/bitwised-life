from os.path import join, dirname

from restfulpy.application import Application


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

    def insert_basedata(self):  # pragma: no cover
        pass

    def insert_mockup(self, *args):  # pragma: no cover
        pass
