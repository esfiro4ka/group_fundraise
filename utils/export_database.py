import datetime
import decimal
import time

import gspread
import gspread_formatting as gspf
from oauth2client.service_account import ServiceAccountCredentials

from config.settings import GOOGLE_SHEET_CREDENTIALS, SHEET_ID

from .database_utils import get_data_from_table, get_table_columns


def export_to_google_sheets():
    """
    Экспортирует данные из базы данных в Google Sheets.

    Подключается к Google Sheets API, создает новые листы для таблицы
    "Collects" и "Payments",
    извлекает данные из базы данных и записывает их в соответствующие листы.
    """

    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_SHEET_CREDENTIALS, scope)

    client = gspread.authorize(creds)

    spreadsheet_id = SHEET_ID
    spreadsheet = client.open_by_key(spreadsheet_id)

    sheet1 = spreadsheet.add_worksheet(title='Collects', rows=None, cols=None)
    sheet2 = spreadsheet.add_worksheet(title='Payments', rows=None, cols=None)

    header_row_data_table1 = get_table_columns('collects_collect')
    header_row_data_table2 = get_table_columns('payments_payment')

    def bold_insert_row(sheet, header_row_data_table, index=1):
        """Вставляет названия колонок жирным шрифтом."""

        sheet.insert_row(header_row_data_table, index)
        bold_format = gspf.cellFormat(textFormat=gspf.TextFormat(bold=True))
        gspf.format_cell_range(sheet, f'A{index}:ZZ{index}', bold_format)

    bold_insert_row(sheet1, header_row_data_table1, index=1)
    bold_insert_row(sheet2, header_row_data_table2, index=1)

    def serialize_value(value):
        """Преобразует данные в формат, пригодный для сериализации в JSON."""

        if isinstance(value, decimal.Decimal):
            return float(value)
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return value

    def insert_data_to_sheet(data, sheet):
        """Вставляет данные."""

        for row_num, row_data in enumerate(data, start=2):
            row_data_serialized = [
                serialize_value(value) for value in row_data]
            sheet.insert_row(row_data_serialized, index=row_num)
            time.sleep(5)

    data_table1 = get_data_from_table('collects_collect')
    data_table2 = get_data_from_table('payments_payment')

    insert_data_to_sheet(data_table1, sheet1)
    insert_data_to_sheet(data_table2, sheet2)
