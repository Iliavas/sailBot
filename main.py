import telebot
from config import BOT_TOKEN
from keyboards import Keyboard

from logic import get_products, \
    get_trash_ids, \
    get_product, \
    remove_trash, \
    get_cost, \
    get_list_of_orders, \
    create_order, \
    add_to_trash
from collections.abc import Iterable

app = telebot.TeleBot(BOT_TOKEN)


@app.message_handler(commands=["start"])
def start(info):
    app.send_message(info.chat.id,
                     "Приветствую тебя в боте для ресторанов",
                     reply_markup=Keyboard.base_keyboard()
                     )


@app.message_handler(func=lambda m: m.text == "Посмотреть меню")
def show_products(info):
    products = get_products()
    for product in products:
        app.send_photo(
            info.chat.id,
            product.image,
            caption=
            "Имя: {}\nЦена: {}р\nВремя приготовления:{}\n{}".format(
                product.name,
                product.costRubles,
                product.timeCooked,
                product.description
            ),
            reply_markup=Keyboard.product_inline_keyboard(product.id, info.from_user.id)
        )


@app.message_handler(func=lambda m: m.text == "Посмотреть корзину")
def show_trash(info):
    app.send_message(
        info.chat.id,
        "Ваша корзина:",
        reply_markup=Keyboard.trash_keyboard()
    )
    products_ids, error = get_trash_ids(info.from_user.id)
    if isinstance(products_ids, Iterable):
        for product in map(
                lambda product_id: get_product(product_id),
                products_ids
        ):
            app.send_photo(
                info.chat.id,
                product.image,
                caption=product.description,
                reply_markup=Keyboard.delete_inline_keyboard(
                    str(product.id),
                    info.from_user.id
                )
            )
    else:
        app.send_message(
            info.chat.id,
            error,

        )


@app.message_handler(func=lambda m: m.text == "Очистить корзину")
def show_remove_trash(info):
    message_to_user = remove_trash(info.from_user.id)
    app.send_message(info.chat.id, message_to_user)


@app.message_handler(func=lambda m: m.text == "Посмотреть стоимость")
def show_cost(info):
    cost = get_cost(info.from_user.id)
    app.send_message(info.chat.id, cost)


@app.message_handler(func=lambda m: m.text == "Назад")
def change_keyboard_to_base(info):
    app.send_message(
        info.chat.id,
        "Вы перешли в главное меню",
        reply_markup=Keyboard.base_keyboard())


@app.message_handler(func=lambda m: m.text == "Список заказов")
def show_list_of_orders(info):
    orders = get_list_of_orders()
    for order in orders:
        app.send_message(
            info.chat.id,
            "Заказ стоимостью: {}р\nВремя приготовления: {}".format(
                order.costRubles,
                order.time_to_cook,
            )
        )


@app.message_handler(func=lambda m: m.text == "Заказать")
def order(info):
    order_message = create_order(info.from_user.id)
    app.send_message(info.chat.id, order_message)


@app.callback_query_handler(func=lambda m: m.data.split()[0] == "delete")
def delete_from_trash(message):
    delete_from_trash(message.data.split()[1], message.data.split()[2])
    app.send_message(message.message.chat.id, "Продукт успешно удален")
    app.answer_callback_query(message.id)


@app.callback_query_handler(func=lambda m: m.data.split()[0] == "add")
def show_add_to_trash(message):
    add_to_trash(message.data.split()[1], message.data.split()[2])
    app.send_message(message.message.chat.id, "Продукст успешно добавлен")
    app.answer_callback_query(message.id)


if __name__ == "__main__":
    while True:
        app.polling(none_stop=True)