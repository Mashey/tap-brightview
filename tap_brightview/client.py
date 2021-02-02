from dotenv import load_dotenv
import os
import jaydebeapi
import jpype

class HiveClient:
    def __init__(self):
        load_dotenv()
        BV_USER = os.getenv("BV_USER")
        BV_PASSWORD = os.getenv("BV_PASSWORD")
        self.client = jaydebeapi.connect(
            "com.simba.hive.jdbc.HS2Driver",
            "jdbc:hive2://bdgw.qualifacts.org:443/brightview_prod;ssl=1;transportMode=http;httpPath=gateway/default/llap",
            [BV_USER, BV_PASSWORD],
            "./HiveJDBC42.jar",
        )
        self.sql = self.client.cursor()

    def query_database(self, table, last_operation_time='2000-01-11 00:00:00.000000'):
        self.sql.execute(
            'SELECT * ' +
            f'FROM {table} ' +
            f'WHERE last_operation_time >= "{last_operation_time}"' +
            'ORDER BY last_operation_time ' +
            'LIMIT 15'
        )

        query = self.sql.fetchall()

        return query


# client = HiveClient()
# new_stream = stream.ActProcMatrixDsc(client)
# response = client.query_database('activity')
# test = 'test'
