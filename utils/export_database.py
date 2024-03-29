import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config.settings import GOOGLE_SHEET_CREDENTIALS, SHEET_ID

from .database_utils import get_data_from_all_tables


def export_to_google_sheets():
    data = get_data_from_all_tables()

    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_SHEET_CREDENTIALS, scope)

    client = gspread.authorize(creds)

    spreadsheet_id = SHEET_ID
    sheet = client.open_by_key(spreadsheet_id).sheet1

    for row_num, row_data in enumerate(data, start=1):
        row_data_serialized = []
        for item in row_data:
            if isinstance(item, datetime.datetime):
                row_data_serialized.append(item.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                row_data_serialized.append(item)
        try:
            sheet.insert_row(row_data_serialized, index=row_num)
        except Exception as e:
            print(f'Error inserting row {row_num}: {e}')

    print('Data exported to Google Sheets successfully.')
