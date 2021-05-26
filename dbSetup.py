from models import db, Product
import datetime

with open("images/morkov.jpg", "rb") as f:
    product = Product.create(name="Морковка", description="Это сочная морковка", costRubles=120, image=f.read(), timeCooked=datetime.time(hour=0, minute=30, second=0))
    product.save()


with open("images/ogurec.jpg", "rb") as f:
    product = Product.create(name="Огурец", description="Это вкусный огурец", costRubles=100, image=f.read(), timeCooked=datetime.time(hour=0, minute=20, second=30))