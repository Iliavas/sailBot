from models import Product, History, Order
from datetime import time


def get_products():
    '''
    функция возвращающая все продукты
    '''
    return Product.select()


def get_trash_ids(user_id):
    '''
    функция возвращающая id продуктов, заказанных пользователем
    '''
    trash = None,
    error = None
    try:
        trash = History.get(name=user_id)
        if not len(trash.products_id):
            return None, "Вы еще не поместили в корзину ни одного продукта"
    except:
        return None, "У вас в корзине нет ни одного продукта"

    return trash.products_id, error


def get_product(product_id):
    '''
    функция возвращающая продукт по его id
    '''
    return Product.get(id=product_id)


def remove_trash(user_id):
    '''
    функция очищающая корзину
    '''
    message = "Удаление продукта прошло успешно"
    try:
        trash = History.get(name=user_id)
        trash.products_id = []
        trash.save()
    except:
        message = "У вас была пустая корзина"

    return message


def get_cost(user_id):
    '''
    функция, считающая стоимость корзины пользователя
    '''
    try:
        trash = History.get(id=user_id)
        cost = 0
        for product_id in trash.products_id:
            cost += Product.get(id=product_id).costRubles
        return "стоимость корзины: {}р".format(str(cost))
    except:
        return "У вас пустая корзина"


def get_list_of_orders():
    '''
    функция возвращает список заказов
    '''
    orders = Order.select()
    return orders


def create_order(user_id):
    '''
    функция создания заказа
    '''
    try:
        trash = History.get(name=user_id)
        cost = 0
        time_cooked = time(minute=0, second=0)

        if not len(trash.products_id):
            return "У вас пустая корзина"

        for product_id in trash.products_id:
            product = Product.get(id=product_id)
            cost += product.costRubles
            time_cooked = max(time_cooked, product.timeCooked)
        trash.products_id = []
        trash.save()
        Order.create(user_id=user_id, time_to_cook=time_cooked, costRubles=cost)
        return "Заказ будет стоить {}р\nВремя приготовления {}".format(
            cost, time_cooked
        )
    except:
        return "У вас пустая корзина"


def delete_from_trash(user_id, delete_product_id):
    '''
    функция удаления товара из корзины
    '''
    trash = History.get(name=user_id)

    new_ids = []
    is_deleted = False
    for product_id in trash.products_id:
        if not is_deleted and product_id == delete_product_id:
            is_deleted = True
            continue
        new_ids.append(product_id)

    trash.products_id = new_ids
    trash.save()


def add_to_trash(user_id, add_product_id):
    '''
    функция добавления товара в корзину
    '''

    trash = None

    try:
        trash = History.get(name=user_id)
    except:
        trash = History.create(name=user_id)
        trash.save()
    trash.products_id.append(add_product_id)
    trash.save()