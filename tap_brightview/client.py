from dotenv import load_dotenv
import os
import jaydebeapi
import jpype


class HiveClient:
    def __init__(self):
        load_dotenv()
        USER = os.getenv("USER")
        PASSWORD = os.getenv("PASSWORD")
        self.client = jaydebeapi.connect(
            "com.simba.hive.jdbc.HS2Driver",
            "jdbc:hive2://bdgw.qualifacts.org:443/brightview_prod;ssl=1;transportMode=http;httpPath=gateway/default/llap",
            [USER, PASSWORD],
            "./HiveJDBC42.jar",
        )
        self.sql = self.client.cursor()


    def query_database(self):
        self.sql.execute(
            'SELECT * ' +
            'FROM activity ' +
            'LIMIT 0,10'
        )

        query = self.sql.fetchall()

        return query


client = HiveClient()
response = client.query_database()
test = 'test'