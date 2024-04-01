from django.db import connection


def get_table_columns(table_name):
    """Получает имена столбцов указанной таблицы из базы данных."""

    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position""")
        columns = cursor.fetchall()
    return [column[0] for column in columns]


def get_data_from_table(table_name):
    """Получает данные из указанной таблицы базы данных."""

    data = []

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT * FROM {table_name}""")
        data = cursor.fetchall()

    return data
