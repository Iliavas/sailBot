from peewee import *
from playhouse.postgres_ext import ArrayField

db = PostgresqlDatabase(
    'bot',
    user="postgres",
    password="Ilvas2006",
    host="localhost",
    port=5432
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


db.connect()
db.create_tables([Product, History])