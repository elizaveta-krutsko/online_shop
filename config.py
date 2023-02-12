import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('/home/oem/PycharmProjects/online_shop/envs/.env')
load_dotenv(dotenv_path=dotenv_path)

DB_DIALECT: str = os.getenv('DB_DIALECT')  #postgresql
DB_HOST: str = os.getenv('DB_HOST')  #localhost
DB_USERNAME: str = os.getenv('DB_USERNAME')  #online_shop
DB_PASSWORD: str = os.getenv('DB_PASSWORD')  #root
DB_NAME: str = os.getenv('DB_NAME')  #postgres
DB_PORT: str = os.getenv('DB_PORT')  #5432