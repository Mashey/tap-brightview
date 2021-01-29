from dotenv import load_dotenv
import os
import jaydebeapi
import jpype


# This code is for production.
# args = singer.utils.parse_args(["user", "password"])
# USER = args.config['user']
# PASSWORD = args.config['password']

# The code below is for testing with Pytest.
load_dotenv()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


def create_client():
    client = jaydebeapi.connect(
        "com.simba.hive.jdbc.HS2Driver",
        "jdbc:hive2://bdgw.qualifacts.org:443/brightview_prod;ssl=1;transportMode=http;httpPath=gateway/default/llap",
        [USER, PASSWORD],
        "./HiveJDBC42.jar",
    )

    return client


def create_sql_cursor(client):
    sql = client.cursor()

    return sql
