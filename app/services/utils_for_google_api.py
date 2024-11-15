import copy
from datetime import datetime

from app.constants import (COLUMN_COUNT, ROW_COUNT, SPREADSHEET_PATTERN,
                           TABLE_VALUES_PATTERN, TIME_FORMAT_GOOGLE_SHEET)


def set_value_gridProperties(spreadsheet_body, key, value):
    spreadsheet_body['sheets'][0]['properties']['gridProperties'][key] = value


def get_spreadsheet_body(
    current_time=None,
    row_count=ROW_COUNT,
    column_count=COLUMN_COUNT,
):
    if current_time is None:
        current_time = datetime.now()

    current_time = current_time.strftime(TIME_FORMAT_GOOGLE_SHEET)

    spreadsheet_body = copy.deepcopy(SPREADSHEET_PATTERN)

    spreadsheet_body['properties']['title'] = f'Отчет на {current_time}'
    set_value_gridProperties(spreadsheet_body, 'rowCount', row_count)
    set_value_gridProperties(spreadsheet_body, 'columnCount', column_count)

    return spreadsheet_body


def get_table_values():
    table_values = copy.deepcopy(TABLE_VALUES_PATTERN)
    current_time = datetime.now().strftime(TIME_FORMAT_GOOGLE_SHEET)
    table_values[0] = [f'Отчёт от {current_time}']
    return table_values
