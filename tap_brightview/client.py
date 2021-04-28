import jaydebeapi
import jpype
import tap_brightview.helpers as helper
import singer

LOGGER = singer.get_logger()


class HiveClient:
    def __init__(self, config):
        self.BV_USER = config["BV_USER"]
        self.BV_PASSWORD = config["BV_PASSWORD"]
        self.client = self.setup_connection()
        self.sql = self.client.cursor()

    def setup_connection(self):
        connection = jaydebeapi.connect(
            "com.simba.hive.jdbc.HS2Driver",
            "jdbc:hive2://bdgw.qualifacts.org:443/brightview_prod;ssl=1;transportMode=http;httpPath=gateway/default/llap",
            [self.BV_USER, self.BV_PASSWORD],
            "./HiveJDBC42.jar",
        )
        return connection

    def query_database(
        self,
        schema,
        table,
        id,
        limit=1000,
        offset=0,
        limit_key="last_operation_time",
        limit_key_value="1970-01-11 00:00:00.000000",
    ):

        row_count = 0
        order_by = f"ORDER BY {limit_key}, {id} "

        if id == None:
            order_by = f"ORDER BY {limit_key} "
        
        if table == "procedure":
            table = "`procedure`"

        LOGGER.info("Querying DB")
        self.sql.execute(
            "SELECT * "
            + f"FROM {table} "
            + f'WHERE {limit_key} >= "{limit_key_value}" '
            + order_by
            + f"LIMIT {limit} OFFSET {offset}"
        )

        LOGGER.info("Query Complete.  Starting rows")
        row = ""

        while row is not None:
            row_count += 1
            row = self.sql.fetchone()
            if row == None:
                self.sql._close_last()
                return row
            if row_count % 10000 == 0:
                LOGGER.info(f"Row count = {row_count}")
            yield helper.create_json_response(schema, row)
