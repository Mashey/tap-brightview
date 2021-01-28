import tap_brightview.service as service


client = service.create_client()
sql = service.create_sql_cursor(client)


def query_database():
    sql.execute(
        'SELECT * ' +
        'FROM activity ' +
        'LIMIT 0,10'
    )

    query = sql.fetchall()

    return query


sql.close()
client.close()
