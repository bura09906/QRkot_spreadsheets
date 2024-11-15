MIN_LENGH_STR_FIELD = 1
MAX_LENGH_FIELD_NAME = 100
DEFAULT_INVESTED_AMOUNT = 0
THRESHOLD_FULL_AMOUNT = 0

ROW_COUNT = 100
COLUMN_COUNT = 11
TIME_FORMAT_GOOGLE_SHEET = "%Y/%m/%d %H:%M:%S"

SPREADSHEET_PATTERN = {
    'properties': {'title': None,
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': None,
                                                  'columnCount': None}}}]
}

TABLE_VALUES_PATTERN = [
    [],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
