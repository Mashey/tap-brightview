import singer
import json
from singer import Transformer, metadata, bookmarks
import tap_brightview.helpers as helper
from tap_brightview.client import HiveClient
from tap_brightview.streams import STREAMS


LOGGER = singer.get_logger()


def sync(config, state, catalog):
    client = HiveClient()

    with Transformer() as transformer:
        for stream in catalog.get_selected_streams(state):
            tap_stream_id = stream.tap_stream_id
            stream_obj = STREAMS[tap_stream_id](client, state)
            replication_key = stream_obj.replication_key
            stream_schema = stream.schema.to_dict()
            stream_metadata = metadata.to_map(stream.metadata)

            LOGGER.info(f'Staring sync for stream: {tap_stream_id}')

            LOGGER.info(f'Setting initial state: {state}')
            state = singer.set_currently_syncing(state, tap_stream_id)
            singer.write_state(state)
            singer.write_schema(
                tap_stream_id,
                stream_schema,
                stream_obj.key_properties,
                stream.replication_key
            )
            state_file = helper.open_state_file()

            # Something that concerns me a bit is when the state.json file is opened in write mode
            # it clears all existing data from the file. The state_file variable contains the existing
            # state.json data as a dict. My concern is if the record loop exits before writing a new bookmark,
            # how do we ensure state.json has the necessary bookmarks?
            with open('./state.json', 'w') as current_state:

                for record in stream_obj.records_sync(table_name=tap_stream_id):
                    transformed_record = transformer.transform(
                        record, stream_schema, stream_metadata)

                    LOGGER.info(f"Writing record: {transformed_record}")
                    singer.write_record(
                        tap_stream_id,
                        transformed_record,
                    )
                    singer.write_bookmark(
                        stream_obj.state,
                        tap_stream_id,
                        replication_key,
                        record['last_operation_time']
                    )
                    singer.write_state(
                        {'last_operation_time': record['last_operation_time']}
                    )

                # I had to move the bookmark creation block out of the record loop
                # If the block is moved in the record loop a bookmark is added to state.json for each record
                # This means that we can only bookmark after a successful batch, which kind of makes me nervous
                # However, it might not be a big deal if an error occurs and we exit the loop
                # If we can find a way to create the bookmark after each record that would be cool, BUT
                # I don't want to spend forever trying to figure it out
                LOGGER.info(f'Creating bookmark for {tap_stream_id} stream in state.json')
                bookmark = singer.get_bookmark(
                    state,
                    tap_stream_id,
                    replication_key
                )
                state_file["bookmarks"][tap_stream_id][replication_key] = bookmark
                new_state = json.dumps(state_file, indent=4)
                current_state.write(new_state)
                LOGGER.info(f'Bookmark created for {tap_stream_id} stream = {replication_key}: {bookmark}')


    state = singer.set_currently_syncing(state, None)
    # singer.write_state(state)
