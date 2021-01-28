def create_table_list(tables_path):
    with open(f'{tables_path}') as tables:
        table_data = tables.readlines()

    clean_data = []

    for row in table_data:
        clean_data.append(row.rstrip())

    return clean_data
