from celery import Celery
import config
from sql_online_shop import crud
from fastapi import Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from celery.utils.log import get_task_logger

celery = Celery("celery_worker", broker='redis://localhost:6379')
celery.conf.broker_url = config.CELERY_BROKER_URL
celery.conf.result_backend = config.CELERY_RESULT_BACKEND


# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)


@celery.task(name="remove_expired_orders_tasks")
def remove_expired_orders_tasks(db: Session = Depends(get_db)):
    crud.remove_expired_orders(db=db)


# Display log
    celery_log.info(f"Clearing Completed!")


#celery.conf.beat_schedule = {
#    'task-name': {
#        #'task': 'tasks.remove_expired_orders_tasks',
#        'task': 'tasks.print_hi',
#        'schedule': 15.0,
#        'args': (2,),
#    },
#}
#celery.conf.timezone = 'UTC'