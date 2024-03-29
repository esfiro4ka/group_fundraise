from django.db import connection


def get_all_table_names():
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'""")
        table_names = cursor.fetchall()

    return [name[0] for name in table_names]


def get_data_from_all_tables():
    all_data = []

    table_names = get_all_table_names()

    for table_name in table_names:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {table_name}')
            data = cursor.fetchall()
            all_data.extend(data)

    return all_data
