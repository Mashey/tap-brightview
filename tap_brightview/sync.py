import singer
import json
from singer import Transformer, metadata, bookmarks
import tap_brightview.helpers as helper
import time


LOGGER = singer.get_logger()


def sync(config, state, catalog, stream_collection):
    with Transformer() as transformer:
        for stream in catalog.get_selected_streams(state):
            start = time.perf_counter()
            records_written = 0
            tap_stream_id = stream.tap_stream_id
            stream_obj = stream_collection[tap_stream_id](state, config)
            replication_key = stream_obj.replication_key
            stream_schema = stream.schema.to_dict()
            stream_metadata = metadata.to_map(stream.metadata)

            LOGGER.info(f'Staring sync for stream: {tap_stream_id}')

            singer.set_currently_syncing(state, tap_stream_id)
            singer.write_state(state)
            singer.write_schema(
                tap_stream_id,
                stream_schema,
                stream_obj.key_properties,
                stream.replication_key
            )

            for record in stream_obj.records_sync():
                transformed_record = transformer.transform(
                    record, stream_schema, stream_metadata)

                # LOGGER.info(f"Writing record: {records_written}")
                singer.write_record(
                    tap_stream_id,
                    transformed_record,
                )
                records_written += 1


            if records_written == 0:
                LOGGER.info(
                    f'No records found for {tap_stream_id}')
            else:
                stop = time.perf_counter()
                elasped_time = stop - start
                LOGGER.info(f'{tap_stream_id} completed in {elasped_time:0.4f} seconds. {elasped_time / records_written} rps')
                LOGGER.info(
                    f'Number of Records: {records_written}')
                singer.write_bookmark(
                    state,
                    tap_stream_id,
                    replication_key,
                    record[stream_obj.replication_key]
                )
                    


    state = singer.set_currently_syncing(state, None)
    singer.write_state(state)
