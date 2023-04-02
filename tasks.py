from celery import Celery
from sql_online_shop import crud
from sqlalchemy.orm import Session


celery = Celery("tasks", broker='redis://localhost:6379')


@celery.task
def remove_expired_orders_tasks(db: Session):
    crud.remove_expired_orders(db=db)
