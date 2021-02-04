import singer
import json
from singer import Transformer, metadata, bookmarks
import tap_brightview.helpers as helper
from tap_brightview.streams import STREAMS


LOGGER = singer.get_logger()


def sync(config, state, catalog):
    with Transformer() as transformer:
        for stream in catalog.get_selected_streams(state):
            records_written = 0
            tap_stream_id = stream.tap_stream_id
            stream_obj = STREAMS[tap_stream_id](state)
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
                try:
                    for record in stream_obj.records_sync():
                        transformed_record = transformer.transform(
                            record, stream_schema, stream_metadata)

                        LOGGER.info(f"Writing record: {transformed_record}")
                        singer.write_record(
                            tap_stream_id,
                            transformed_record,
                        )
                        records_written += 1
                        singer.write_bookmark(
                            stream_obj.state,
                            tap_stream_id,
                            replication_key,
                            record[stream_obj.replication_key]
                        )

                except:
                    LOGGER.info(f'An Error happened during {tap_stream_id} stream.')
                    continue
                finally:
                    bookmark = singer.get_bookmark(
                        state,
                        tap_stream_id,
                        replication_key
                    )
                    state_file["bookmarks"][tap_stream_id][replication_key] = bookmark
                    new_state = json.dumps(state_file, indent=4)
                    current_state.write(new_state)
                    LOGGER.info(
                        f'Bookmark created for {tap_stream_id} stream = {replication_key}: {bookmark}')


            # I had to move the bookmark creation block out of the record loop
            # If the block is moved in the record loop a bookmark is added to state.json for each record
            # This means that we can only bookmark after a successful batch, which kind of makes me nervous
            # However, it might not be a big deal if an error occurs and we exit the loop
            # If we can find a way to create the bookmark after each record that would be cool, BUT
            # I don't want to spend forever trying to figure it out

            if records_written == 0:
                LOGGER.info(
                    f'No records found for {tap_stream_id}')
            else:
                LOGGER.info(
                    f'Number of Records: {records_written}')


    state = singer.set_currently_syncing(state, None)
    # singer.write_state(state)
