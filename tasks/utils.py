import logging

logger = logging.getLogger(__name__)



def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

from django.db import connection

def execute_select(query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
    except Exception:
        logger.exception("Error in excute_select")



def execute_query(query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
    except Exception:
        logger.exception("Error in excute_query")

