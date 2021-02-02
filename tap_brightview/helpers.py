import json
import tap_brightview.service as service
from schema_builder import build_json_schema


def create_table_list(tables_path):
    with open(f'{tables_path}') as tables:
        table_data = tables.readlines()

    clean_data = []

    for row in table_data:
        clean_data.append(row.rstrip())

    return clean_data


def create_json_schemas(file_path):
    table_list = create_table_list(file_path)
    client = service.create_client()
    sql = service.create_sql_cursor(client)

    for table in table_list:
        sql.execute(f"DESCRIBE FORMATTED brightview_prod.{table}")
        query = sql.fetchall()

        build_json_schema('table', data=query, table_name=table)

    return 'JSON Schemas created successfully.'


def open_json_schema(table_name):
    with open(f'./tap_brightview/schemas/{table_name}_schema.json') as schema:
        json_schema = json.load(schema)

    return json_schema


def create_json_response(json_schema, response):
    schema_keys = list(json_schema['properties'])
    json_response = []

    for row in response:
        key_value_pairs = list(zip(schema_keys, row))
        schema_properties = {}

        for pair in key_value_pairs:
            schema_properties[pair[0]] = pair[1]

        json_response.append(schema_properties)

    return json_response
