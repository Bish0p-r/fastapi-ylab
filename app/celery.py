from celery import Celery

from app.config import settings

celery = Celery('celery', include=['app.tasks.excel_to_db'])
celery.conf.broker_url = settings.rabbitmq_amqp_url
celery.conf.result_backend = settings.rabbitmq_rpc_url
celery.conf.beat_schedule = {
    'synchronization_excel_to_db': {'task': 'app.tasks.excel_to_db.synchronization_excel_to_db', 'schedule': 15.0}
}
