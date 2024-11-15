from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services.utils_for_google_api import (get_spreadsheet_body,
                                               get_table_values)


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    row_count: int
) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = get_spreadsheet_body(row_count=row_count)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
):
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = get_table_values()

    for project in projects:
        new_row = [
            project['name'],
            str(project['closing_time']),
            project['description'],
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'R1C1:R{len(table_values)}C3',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
