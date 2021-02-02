import singer
import tap_brightview.helpers as helper

LOGGER = singer.get_logger()


class Stream:
    tap_stream_id = None
    key_properties = []
    replication_method = ''
    valid_replication_keys = []
    replication_key = 'last_updated_at'
    object_type = ''
    selected = True

    def __init__(self, client, state):
        self.client = client
        self.state = state

    def sync(self, *args, **kwargs):
        raise NotImplementedError("Sync of child class not implemented")


class IncrementalStream(Stream):
    replication_method = 'INCREMENTAL'


class FullTableStream(Stream):
    replication_method = 'FULL_TABLE'


class ActProcMatrixDsc(IncrementalStream):
    table_name = 'act_proc_matrix_dsc'
    tap_stream_id = 'act_proc_matrix_dsc'
    key_properties = ['act_proc_matrix_dsc_id']
    replication_method = 'INCREMENTAL'
    valid_replication_keys = ['last_operation_time']
    replication_key = 'last_operation_time'

    def records_sync(self, table_name):
        json_schema = helper.open_json_schema(table_name)
        response = self.client.query_database()
        json_response = helper.create_json_response(json_schema, response)
        for row in json_response:
          yield row


STREAMS = {
    'act_proc_matrix_dsc': ActProcMatrixDsc
}
