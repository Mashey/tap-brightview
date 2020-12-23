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


def parse_table_schema(table=None):
    sql.execute("DESCRIBE FORMATTED brightview_prod.activity")
    query = sql.fetchall()
    table_columns = parse_formatted_table(query)

    return table_columns


def parse_formatted_table(table):
    end_data_index = table.index(('', None, None))
    clean_table = table[1:end_data_index]
    parsed_table = []

    for row in clean_table:
        parsed_table.append([row[0], row[1]])
    
    return parsed_table


# db_tables = find_database_tables()
table_schema = parse_table_schema()

stop = 'stop'

sql.close()
client.close()
