from celery import Celery
import config
from sql_online_shop import crud
from dependencies import get_db
from celery.utils.log import get_task_logger

celery = Celery("celery", broker='redis://redis:6379')
celery.conf.broker_url = config.CELERY_BROKER_URL
celery.conf.result_backend = config.CELERY_RESULT_BACKEND

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)


@celery.task(name="celery.remove_expired_orders_tasks")
def remove_expired_orders_tasks():
    crud.remove_expired_orders(db=next(get_db()))


# Display log
    celery_log.info(f"Clearing Completed!")


celery.conf.beat_schedule = {
    'task-name': {
        'task': 'celery.remove_expired_orders_tasks',
        'schedule': 7200.0,
    }
}
celery.conf.timezone = 'UTC'
