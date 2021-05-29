from peewee import *
from playhouse.postgres_ext import ArrayField

from config import DB_HOST, DB_NAME, DB_PORT, DB_USER, DB_PASSWORD

db = PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    name = TextField()
    description = TextField()
    timeCooked = TimeField()
    costRubles = IntegerField()
    image = BlobField()


class History(BaseModel):
    products_id = ArrayField(TextField)
    name = TextField()


class Order(BaseModel):
    user_id = TextField()
    time_to_cook = TimeField()
    costRubles = IntegerField()


db.connect()
db.create_tables([Product, History, Order])