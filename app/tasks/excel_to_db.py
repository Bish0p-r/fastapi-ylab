import asyncio

from app.celery import celery
from app.common.utils.db import scoped_session
from app.common.utils.excel_parser import get_parsed_data
from app.dependencies.admin import admin_services
from app.services.cache import cache_service


async def start_synchronization_excel_to_db(parsed_data: dict) -> None:
    await cache_service.setup()
    async with scoped_session() as session:
        await admin_services.start_sync(session, parsed_data)


@celery.task
def synchronization_excel_to_db() -> None:
    parsed_data = get_parsed_data()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_synchronization_excel_to_db(parsed_data))
