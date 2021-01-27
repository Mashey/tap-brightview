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
USER = json.loads(os.getenv("brightview"))['user']
PASSWORD = json.loads(os.getenv("brightview"))['password']


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
    table_list = create_table_list()
    for table in table_list:
        sql.execute(f"DESCRIBE FORMATTED brightview_prod.{table}")
        query = sql.fetchall()
        table_columns = parse_formatted_table(query, table)
        # From the Schema Builder package import build_json_schema
        # return build_json_schema('table', data=table_columns, table_name=table)

    return table_columns


def create_table_list():
    with open('./test_tables.txt') as tables:
        table_data = tables.readlines()

    clean_data = []

    for row in table_data:
        clean_data.append(row.rstrip())

    return clean_data


def parse_formatted_table(table_data, table):
    end_data_index = table_data.index(('', None, None))
    clean_table_data = table_data[1:end_data_index]
    parsed_table_data = []

    for row in clean_table_data:
        parsed_table_data.append([row[0], row[1]])

    return parsed_table_data, table


# db_tables = find_database_tables()
table_schema = parse_table_schema()

stop = 'stop'

sql.close()
client.close()
