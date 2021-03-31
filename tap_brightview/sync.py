import singer
import json
from singer import Transformer, metadata, bookmarks
import tap_brightview.helpers as helper
import time


LOGGER = singer.get_logger()


def sync(config, state, catalog, stream_collection):
    total_records = []
    stream_rps = []

    with Transformer() as transformer:
        for stream in catalog.get_selected_streams(state):
            start = time.perf_counter()
            records_written = 0
            tap_stream_id = stream.tap_stream_id
            stream_obj = stream_collection[tap_stream_id](state, config)
            replication_key = stream_obj.replication_key
            stream_schema = stream.schema.to_dict()
            stream_metadata = metadata.to_map(stream.metadata)

            LOGGER.info(f"Staring sync for stream: {tap_stream_id}")

            singer.set_currently_syncing(state, tap_stream_id)
            singer.write_state(state)
            singer.write_schema(
                tap_stream_id,
                stream_schema,
                stream_obj.key_properties,
                stream.replication_key,
            )

            for record in stream_obj.records_sync():
                transformed_record = transformer.transform(
                    record, stream_schema, stream_metadata
                )

                singer.write_record(
                    tap_stream_id,
                    transformed_record,
                )
                records_written += 1

            if records_written == 0:
                LOGGER.info(f"No records found for {tap_stream_id}")
            else:
                info, rps = metrics(
                    start=start, end=time.perf_counter(), records=records_written
                )
                stream_rps.append(rps)
                LOGGER.info(f"{info}")
                singer.write_bookmark(state, tap_stream_id, "metrics", info)

                singer.write_bookmark(
                    state,
                    tap_stream_id,
                    replication_key,
                    record[stream_obj.replication_key],
                )

    state = singer.set_currently_syncing(state, None)
    overall_rps = overall_metrics(total_records, stream_rps)
    singer.write_bookmark(
        state,
        "Overall",
        "metrics",
        f"Records: {sum(total_records)} / RPS: {overall_rps:0.6}",
    )
    singer.write_state(state)


def metrics(start: float, end: float, records: int):
    elapsed_time = end - start
    rps = records / elapsed_time
    info = f"Stream runtime: {elapsed_time:0.6} seconds / Records: {records} / RPS: {rps:0.6}"
    return info, rps


def overall_metrics(records: list, rps_list: list) -> float:
    stream_count = len(records)
    total_rps = sum(rps_list)
    return total_rps / stream_count
