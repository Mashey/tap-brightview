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
    query = sql.execute("SELECT * FROM customer LIMIT 500")

    return query


test = 'wow'

sql.close()
client.close()
 