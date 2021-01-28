import pytest
from tap_brightview.helpers import create_table_list


def test_create_table_list():
    tables = create_table_list('db_tables.txt')

    assert isinstance(tables, list)
    assert len(tables) > 0
    assert isinstance(tables[0], str)
