import os
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), 'envs/.env')
load_dotenv(dotenv_path=dotenv_path)

DB_DIALECT: str = os.getenv('DB_DIALECT')
DB_HOST: str = os.getenv('DB_HOST')
DB_USERNAME: str = os.getenv('DB_USERNAME')
DB_PASSWORD: str = os.getenv('DB_PASSWORD')
DB_NAME: str = os.getenv('DB_NAME')
DB_PORT: str = os.getenv('DB_PORT')
JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY: str = os.getenv('JWT_REFRESH_SECRET_KEY')
CELERY_BROKER_URL: str = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND: str = os.getenv('CELERY_RESULT_BACKEND')
