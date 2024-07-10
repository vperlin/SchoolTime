from contextlib import contextmanager
import psycopg
import sys


@contextmanager
def connect(row_factory=psycopg.rows.dict_row):
    connection = psycopg.connect('service=sch_schooler')
    try:
        yield connection.cursor(row_factory=row_factory)
    finally:
        _, exc_val, _ = sys.exc_info()
        if exc_val:
            connection.rollback()
        else:
            connection.commit()
        connection.close()
