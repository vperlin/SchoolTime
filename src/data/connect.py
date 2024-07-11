from contextlib import contextmanager, suppress
import sys
import psycopg


class Rollback(Exception):
    pass


def rollback():
    raise Rollback()


@contextmanager
def connect(cls=None, *, as_tuples=False):
    if as_tuples:
        rf = psycopg.rows.tuple_row
    elif cls:
        rf = psycopg.rows.class_row(cls)
    else:
        rf = psycopg.rows.dict_row
    # @TODO Набор параметров подключения задавать в настройках
    connection = psycopg.connect('service=sch_schooler')
    with suppress(Rollback):
        try:
            yield connection.cursor(row_factory=rf)
        finally:
            _, exc_value, _ = sys.exc_info()
            if exc_value:
                connection.rollback()
            else:
                connection.commit()
            connection.close()
