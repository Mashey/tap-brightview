import singer
import json
import tap_brightview.helpers as helper
import tap_brightview.client as client

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
        # Add state back as a parameter after testing
        self.state = state

    def sync(self, *args, **kwargs):
        raise NotImplementedError("Sync of child class not implemented")


class IncrementalStream(Stream):
    replication_method = 'INCREMENTAL'


class FullTableStream(Stream):
    replication_method = 'FULL_TABLE'


class Activity(IncrementalStream):
    hive_client = client.HiveClient()
    table_name = 'activity'
    tap_stream_id = 'activity'
    key_properties = ['activity_id']
    replication_method = 'INCREMENTAL'
    valid_replication_keys = ['last_operation_time']
    replication_key = 'last_operation_time'

    def records_sync(self, table_name):
        json_schema = helper.open_json_schema(table_name)
        response_length = 25
        while response_length >= 25:
            response = self.hive_client.query_database(table_name)
            response_length = len(response)
            json_response = helper.create_json_response(json_schema, response)
            for row in json_response:
                singer.write_bookmark(
                    self.state,
                    self.tap_stream_id,
                    self.replication_key,
                    row['last_operation_time']
                )
                singer.write_state(
                    {'last_operation_time': row['last_operation_time']})

                yield row


def create_state():
    with open('./state.json') as state_file:
        state = json.load(state_file)

        return state


state = create_state()
activity_stream = Activity('dummy', state)

activity_stream.records_sync('activity')

STREAMS = {
    'activity': Activity
}
