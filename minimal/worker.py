import time

from restfulpy.orm import create_thread_unsafe_session

from .cell import Cell


def worker():
    isolated_session = create_thread_unsafe_session()

    while True:
        try:
            cell = Cell.pop(session=isolated_session)
            assert cell is not None
        except :
            isolated_session.rollback()
            continue

        cell.execute()
        if isolated_session.is_active:
            isolated_session.commit()

        time.sleep(.01)
