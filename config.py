import os
import dotenv

dotenv.load_dotenv(".env")


BOT_TOKEN = os.environ["BOT_TOKEN"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]