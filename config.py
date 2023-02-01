import os
from dotenv import load_dotenv

load_dotenv()

DB_DIALECT: str = os.getenv('DB_DIALECT')  #postgresql
DB_HOST: str = os.getenv('DB_HOST')  #localhost
DB_USERNAME: str = os.getenv('DB_USERNAME')  #online_shop
DB_PASSWORD: str = os.getenv('DB_PASSWORD')  #root
DB_NAME: str = os.getenv('DB_NAME')  #postgres
DB_PORT: int = os.getenv('DB_PORT')  #5432