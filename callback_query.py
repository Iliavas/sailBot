from main import app

from keyboards import Keyboard
from models import Product, History
from messageTemplates import MessageTemplate


@app.callback_query_handler(func=lambda m : m.data.split()[0] == "delete")
def deleteFromTrash(message):

    history = History.get(name=message.data.split()[2])
    
    new_ids = []
    flag = False


    for i in history.products_id:
        if i == message.data.split()[1] and not flag:
            flag = True
            continue
        new_ids.append(i)
    
    history.products_id = new_ids
    history.save()


    app.send_message(message.message.chat.id, "Продукт успешно удален из корзины")
    app.answer_callback_query(message.id)


@app.callback_query_handler(func=lambda m: m.data.split()[0] == "add")
def addToTrash(message):
    history = None
    try:
        history = History.get(name=message.data.split()[2])
    except: pass
    if not history:
        history = History.create(name=message.data.split()[2], products_id=[])
    print(history.products_id)
    history.products_id.append(message.data.split(" ")[1])
    history.save()
    app.send_message(message.message.chat.id, "Продукт успешно добавлен в корзину")
    app.answer_callback_query(message.id)
