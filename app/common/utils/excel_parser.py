from decimal import Decimal
from urllib.error import HTTPError

import pandas as pd
from celery.utils.log import get_task_logger

from app.config import settings

logger = get_task_logger(__name__)


def parse_data(df: pd.DataFrame) -> dict[str, list[dict[str, str | Decimal]]]:
    parsed_data: dict[str, list[dict[str, str | Decimal]]] = {'menus': [], 'submenus': [], 'dishes': []}
    current_menu = None
    current_submenu = None

    for n, row in df.iterrows():
        if not pd.isna(row[df.columns[0]]):
            current_menu = {
                'id': str(row[df.columns[0]]),
                'title': row[df.columns[1]],
                'description': row[df.columns[2]]
            }
            parsed_data['menus'].append(current_menu)
            current_submenu = None

        elif not pd.isna(row[df.columns[1]]) and current_menu:
            current_submenu = {
                'id': str(row[df.columns[1]]),
                'menu_id': current_menu['id'],
                'title': row[df.columns[2]],
                'description': row[df.columns[3]]
            }
            parsed_data['submenus'].append(current_submenu)

        elif not pd.isna(row[df.columns[2]]) and current_submenu:
            current_dish = {
                'id': str(row[df.columns[2]]),
                'submenu_id': current_submenu['id'],
                'title': row[df.columns[3]],
                'description': row[df.columns[4]],
                'price': Decimal(row[df.columns[5]]).quantize(Decimal('1.00')),
                'discount': int(row[df.columns[6]]) if not pd.isna(row[df.columns[6]]) else 0
            }
            parsed_data['dishes'].append(current_dish)

    return parsed_data


def get_parsed_data(file_path: str = settings.google_sheets_url) -> dict[str, list[dict[str, str | Decimal]]]:
    try:
        df = pd.read_excel(file_path, header=None)
        logger.info('Get parsed data from Google Sheets')
    except HTTPError:
        logger.info('Can\'t get parsed data from Google Sheets')
        df = pd.read_excel('admin/Menu.xlsx', header=None)
        logger.info('Get parsed data from local file')
    return parse_data(df)
