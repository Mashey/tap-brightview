import singer
from singer.catalog import write_catalog
from tap_brightview.discovery import discover
from tap_brightview.sync import sync
from tap_brightview.streams import STREAMS

# Fill in any required config keys from the config.json here
REQUIRED_CONFIG_KEYS = ["BV_USER", "BV_PASSWORD"]

LOGGER = singer.get_logger()


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    catalog = args.catalog if args.catalog else discover()

    if args.discover:
        write_catalog(catalog)
    else:
        sync(args.config, args.state, catalog, stream_collection=STREAMS)


if __name__ == '__main__':
    main()
