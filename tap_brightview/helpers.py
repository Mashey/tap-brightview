import tap_brightview.service as service
from schema_builder import build_json_schema


def create_table_list(tables_path):
    with open(f'{tables_path}') as tables:
        table_data = tables.readlines()

    clean_data = []

    for row in table_data:
        clean_data.append(row.rstrip())

    return clean_data


def create_json_schemas():
    table_list = create_table_list('db_tables.txt')
    client = service.create_client()
    sql = service.create_sql_cursor(client)

    for table in table_list:
        sql.execute(f"DESCRIBE FORMATTED brightview_prod.{table}")
        query = sql.fetchall()

        build_json_schema('table', data=query, table_name=table)

    return 'JSON Schemas created successfully.'
