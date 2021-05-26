from main import app

from keyboards import Keyboard
from models import Product, History, Order

@app.message_handler(commands=["start"])
def start(message):
    app.send_message(message.chat.id, "Приветствую тебя в боте для ресторанов", reply_markup=Keyboard.base_keyboard())


@app.message_handler(func=lambda m: m.text == "Посмотреть меню")
def show_products(message):
    products = Product.select()
    for i in products:
        app.send_photo(
            message.chat.id,
            caption="Имя: {}\nЦена: {}р\nВремя приготовления:{}\n{}".format(i.name, i.costRubles, i.timeCooked, i.description), 
            photo=i.image,
            reply_markup=Keyboard.product_inline_keyboard(str(i.id), str(message.from_user.id))
            )
        app.send_message(message.chat.id, "----")


@app.message_handler(func=lambda m: m.text == "Посмотреть корзину")
def getTrash(message):
    history = None
    print(message.from_user.first_name)

    app.send_message(message.chat.id, "Ваша корзина: ", reply_markup=Keyboard.trash_keyboard())

    try:
        history = History.get(name=message.from_user.id)
    except:
        app.send_message(message.chat.id, "Вы не заказали ни одного продукта")
        return
    
    if len(history.products_id) == 0:
        app.send_message(message.chat.id, "Вы не заказали ни одного продукта")
        return
    
    for i in history.products_id:
        product = Product.get(id=i)
        app.send_photo(
            message.chat.id,
            photo=product.image,
            caption=product.description,
            reply_markup=Keyboard.delete_inline_keyboard(str(product.id), message.from_user.id)
        )

@app.message_handler(func=lambda m: m.text == "Очистить корзину")
def removeTrash(message):
    history = History.get(name=message.from_user.id)
    history.products_id = []
    history.save()
    app.send_message(message.chat.id, "Ваша корзина очищена")


@app.message_handler(func=lambda m: m.text == "Посмотреть стоимость")
def show_cost(message):
    history = History.get(name=message.from_user.id)

    total_cost = 0

    for i in history.products_id:
        product = Product.get(id=i)
        total_cost += product.costRubles
    app.send_message(message.chat.id, "Стоимость ваших продуктов: {}p".format(str(total_cost)))

@app.message_handler(func=lambda m: m.text == "Назад")
def changeKeyboard(message):
    app.send_message(
        message.chat.id, 
        "Вы перешли в главное меню",
        reply_markup=Keyboard.base_keyboard())

@app.message_handler(func=lambda m: m.text == "Список заказов")
def listOfOrders(message):
    orders = Order.select()
    for order in orders:
        app.send_message(
            message.chat.id,
            "Время приготовления заказа: {}\nстоимость: {}р".format(
                order.time_to_cook, order.costRubles
            )
        )

@app.message_handler(func=lambda m: m.text == "Заказать")
def order(message):
    history = History.get(name=message.from_user.id)

    if not len(history.products_id):
        app.send_message(
            message.chat.id,
            "У вас пустая корзина"
        )
        return None

    cost = sum(map(lambda x : Product.get(id=x).costRubles, history.products_id))

    time = max(map(lambda x : Product.get(id=x).timeCooked, history.products_id))

    Order.create(user_id=message.from_user.id, time_to_cook=time, costRubles=cost)
    history.products_id = []
    history.save()
    app.send_message(
        message.chat.id,
        "Заказ на сумму {}\nбудет готов через {}".format(cost, time)
    )