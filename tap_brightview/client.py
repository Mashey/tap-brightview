import jaydebeapi
import jpype


class HiveClient:
    def __init__(self, config):
        self.BV_USER = config["BV_USER"]
        self.BV_PASSWORD = config["BV_PASSWORD"]
        self.client = self.setup_connection()
        self.sql = self.client.cursor()

    def setup_connection(self):
        if jpype.isJVMStarted() and not jpype.isThreadAttachedToJVM():
            jpype.attachThreadToJVM()
            jpype.java.lang.Thread.currentThread().setContextClassLoader(jpype.java.lang.ClassLoader.getSystemClassLoader())
        connection = jaydebeapi.connect(
            "com.simba.hive.jdbc.HS2Driver",
            "jdbc:hive2://bdgw.qualifacts.org:443/brightview_prod;ssl=1;transportMode=http;httpPath=gateway/default/llap",
            [self.BV_USER, self.BV_PASSWORD],
            "./HiveJDBC42.jar",
        )
        return connection

    def query_database(
        self,
        table,
        id,
        limit=1000,
        offset=0,
        limit_key='last_operation_time',
        limit_key_value='1970-01-11 00:00:00.000000'
    ):
        if table == 'procedure':
            self.sql.execute(
                'SELECT * ' +
                f"FROM 'procedure' " +
                f'WHERE {limit_key} >= "{limit_key_value}" ' +
                f'ORDER BY {limit_key}, {id} ' +
                f'LIMIT {limit} OFFSET {offset}'
            )
            query = self.sql.fetchall()
            return query
        elif id == None:
            self.sql.execute(
                'SELECT * ' +
                f'FROM {table} ' +
                f'WHERE {limit_key} >= "{limit_key_value}" ' +
                f'ORDER BY {limit_key} ' +
                f'LIMIT {limit} OFFSET {offset}'
            )
            query = self.sql.fetchall()
            return query
        else:
            self.sql.execute(
                'SELECT * ' +
                f'FROM {table} ' +
                f'WHERE {limit_key} >= "{limit_key_value}" ' +
                f'ORDER BY {limit_key}, {id} ' +
                f'LIMIT {limit} OFFSET {offset}'
            )
            query = self.sql.fetchall()
            return query
