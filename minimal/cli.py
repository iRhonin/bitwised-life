from easycli import Root, Argument, SubCommand

from .worker import worker


class Start(SubCommand):
    __command__ = 'start'

    def __call__(self, *args, **kwargs):
        worker()
