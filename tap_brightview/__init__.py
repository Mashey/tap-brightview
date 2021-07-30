import singer
from singer.catalog import write_catalog
from tap_brightview.discovery import discover
from tap_brightview.sync import sync
from tap_brightview.streams import REQUIRED_TABLES, STREAMS
import datetime
import time

# Fill in any required config keys from the config.json here
REQUIRED_CONFIG_KEYS = ["BV_USER", "BV_PASSWORD"]

LOGGER = singer.get_logger()


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)
    day = datetime.datetime.today().weekday()

    catalog = args.catalog if args.catalog else discover(day)

    if args.discover:
        write_catalog(catalog)
    else:
        start_main_tables = time.perf_counter()
        sync(args.config, args.state, catalog, stream_collection=REQUIRED_TABLES)
        time_lapse = time.perf_counter() - start_main_tables
        # sync(args.config, args.state, catalog, stream_collection=STREAMS[day])

        LOGGER.info(f'Main tables synced in {(time_lapse / 60):0.2} minutes')


if __name__ == "__main__":
    main()
