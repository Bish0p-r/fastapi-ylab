import asyncio
from decimal import Decimal
from urllib.error import HTTPError

import pandas as pd
from celery.utils.log import get_task_logger

from app.celery import celery
from app.common.utils.db import scoped_session
from app.common.utils.excel_parser import parse_data
from app.config import settings
from app.dependencies.admin import admin_services
from app.services.cache import cache_service

logger = get_task_logger(__name__)


def get_parsed_data(file_path: str = settings.google_sheets_url) -> dict[str, list[dict[str, str | Decimal]]]:
    try:
        df = pd.read_excel(file_path, header=None)
        logger.info('Get parsed data from Google Sheets')
    except HTTPError:
        logger.info('Can\'t get parsed data from Google Sheets')
        df = pd.read_excel('admin/Menu.xlsx', header=None)
        logger.info('Get parsed data from local file')
    return parse_data(df)


async def start_synchronization_excel_to_db(parsed_data: dict) -> None:
    await cache_service.setup()
    async with scoped_session() as session:
        await admin_services.start_sync(session, parsed_data)


@celery.task
def synchronization_excel_to_db() -> None:
    parsed_data = get_parsed_data()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_synchronization_excel_to_db(parsed_data))
