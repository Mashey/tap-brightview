import requests
import json
from dotenv import load_dotenv
import os
import pprint
import singer
from singer import Transformer
from datetime import date, datetime, timezone, timedelta
from collections import defaultdict
import jaydebeapi
import jpype
from schema_builder import build_json_schema


pp = pprint.PrettyPrinter(indent=4, depth=3)

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
    sql.execute("SELECT * FROM activity LIMIT 10")
    # sql.execute("SHOW CREATE TABLE activity")
    # sql.execute("SHOW TABLES IN brightview_prod")
    query = sql.fetchall()

    return query


def find_database_tables():
    # I want to find a way to show only the base tables in the database
    # 'SHOW TABLES' returns all tables and views. I want to exclude views.
    # This command for MySQL looked promising but failed: <show full tables where Table_Type = 'BASE TABLE'>

    # sql.execute("show full tables where Table_Type = 'BASE TABLE'")
    sql.execute("SHOW TABLES")
    query = sql.fetchall()

    return query


def parse_table_schema():
    table_list = create_table_list('db_tables.txt')

    for table in table_list:
        sql.execute(f"DESCRIBE FORMATTED brightview_prod.{table}")
        query = sql.fetchall()

        build_json_schema('table', data=query, table_name=table)

    return 'JSON Schemas created successfully.'


def create_table_list(tables_path):
    with open(f'{tables_path}') as tables:
        table_data = tables.readlines()

    clean_data = []

    for row in table_data:
        clean_data.append(row.rstrip())

    return clean_data


# db_tables = find_database_tables()
table_schema = create_table_list('db_tables.txt')

stop = 'stop'

sql.close()
client.close()
