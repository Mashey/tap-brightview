import requests
import json
from dotenv import load_dotenv
import os
import singer
from datetime import date, datetime, timezone, timedelta
from collections import defaultdict
import jaydebeapi
import jpype
from schema_builder import build_json_schema
from tap_brightview.helpers import create_table_list


# This code is for production.
# args = singer.utils.parse_args(["user", "password"])
# USER = args.config['user']
# PASSWORD = args.config['password']

# The code below is for testing with Pytest.
load_dotenv()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


client = jaydebeapi.connect(
    "com.simba.hive.jdbc.HS2Driver",
    "jdbc:hive2://bdgw.qualifacts.org:443/brightview_prod;ssl=1;transportMode=http;httpPath=gateway/default/llap",
    [USER, PASSWORD],
    "./HiveJDBC42.jar",
)

sql = client.cursor()


def query_database():
    sql.execute(
        'SELECT * ' +
        'FROM activity ' +
        'LIMIT 0,10'
    )

    query = sql.fetchall()

    return query


def create_json_schemas():
    table_list = create_table_list('db_tables.txt')

    for table in table_list:
        sql.execute(f"DESCRIBE FORMATTED brightview_prod.{table}")
        query = sql.fetchall()

        build_json_schema('table', data=query, table_name=table)

    return 'JSON Schemas created successfully.'


sql.close()
client.close()
